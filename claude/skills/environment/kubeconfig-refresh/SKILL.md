---
name: kubeconfig-refresh
description: Manage this machine's kubectl config for the user — the split-file kubeconfig layout at ~/.kube/configs/ (auto-loaded via KUBECONFIG in zsh). Refresh a cluster's token when the user pastes a new/refreshed kubeconfig (e.g. after a Rancher token expired, causing "You must be logged in to the server" errors), add a new cluster from pasted YAML, retire old ones. Triggers on the user pasting kubeconfig YAML, or saying things like "這是新的 kubectl config 幫我更新" / "update my kubeconfig".
---

# Kubeconfig Refresh

Personal workflow for the agent to manage this machine's kubectl config.

## The layout (what the agent is managing)

- One file per cluster under `~/.kube/configs/`, named after the cluster.
- `zsh/zshrc` builds `KUBECONFIG` by globbing the dir (`~/.kube/config` +
  `~/.kube/configs/*.yaml`) — a file dropped in is picked up automatically;
  no env-var editing, ever.
- Tokens expire periodically (e.g. Rancher-issued ones look like
  `kubeconfig-u-xxx:xxx`), causing `kubectl` 401/403 "must be logged in"
  errors across all contexts sharing that user token — usually what
  triggers this skill.
- Retired clusters move to `~/.kube/configs/_archive/` — out of the glob,
  kept for reference.

## Refresh a token (the common case)

1. **Identify the cluster** from the pasted YAML's `current-context` /
   `clusters[].name` (e.g. `prod-us-west-1`).
2. **Locate the matching file**: `~/.kube/configs/<name>.yaml`. If no file
   matches, treat it as a new cluster — confirm with the user, then add it.
3. **Back up** the existing file before touching it:
   `cp <name>.yaml <name>.yaml.bak-<date>` (use `dangerouslyDisableSandbox:
   true` — the sandbox denies writes under `~/.kube/configs/` by default).
4. **Diff old vs new.** Usually only `users[].user.token` changed — edit just
   that field with the Edit tool, preserving the rest of the file's existing
   structure/formatting. If more than the token changed, flag it to the user
   instead of silently applying a structural rewrite.
5. **Switch context**: `kubectx <name>` (also needs
   `dangerouslyDisableSandbox: true`).
6. **Verify**: `kubectl -n {namespace} get pods` (whatever namespace is
   relevant to the conversation) and report the result back to the user.

## Add a cluster (new file)

Write the pasted YAML to `~/.kube/configs/<name>.yaml` — the glob picks it
up automatically; no KUBECONFIG edit. Verify per steps 5–6 above.

## Safety rules (when to pause and ask)

- Cluster name in the pasted config matches no existing file and the user
  has not confirmed it is a new cluster.
- More than just the token field changed between old and new config.
- Anything that would rewrite a file's structure instead of editing the one
  changed field.
