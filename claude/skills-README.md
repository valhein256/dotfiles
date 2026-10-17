# Claude Code Skills & Profiles — Layout and Management

This repo manages the personal layer of the Claude Code setup. Team
skills arrive via the team plugin and its local clone — they are NOT
managed here.

## Layout

```
claude/
  CLAUDE.md                  # personal standards (team rules arrive via the
                             #   plugin session hook; this file is overrides only)
  profiles/                  # the report/comment voice system (used by `draft`)
    core.md                  #   floor + cross-channel traits
    message.md               #   chat replies        (seed)
    reporting.md             #   weekly reports      (evidence-grounded)
    tickets-comments-pr.md   #   ticket/PR comments (corpus seed)
    docs.md                  #   long-form docs     (seed)
  skills/                    # personal skills — symlinked into ~/.claude/skills
    communication/draft/     #   drafting harness (channel voice + review gate
                             #   + save-back into profiles/)
    environment/python-uv-deps/
    environment/kubeconfig-refresh/
    environment/dotfiles-setup/    #   staged machine provisioning (this skill
                                  #   drives make install + the Claude layer)
    automation/weekly-report/
  skills-standby/            # verbatim mirrors of team plugin skills (NOT
                             #   symlinked while the plugin exists — see below)
  settings/settings.example  # redacted settings example incl. the skills-sync
                             #   hook
```

`links.conf` is the single source of truth for what gets symlinked into
`~/.claude/` (`make install-dotfiles`).

## Skills index

| Skill | Origin | Trigger | Depends on |
|---|---|---|---|
| `draft` | original (v2, 2026-10-16) | "draft", any external-facing write-up, pasted text to tighten | `profiles/` (core + channel) |
| `python-uv-deps` | original | any Python work | `team-python-standards` (plugin) when present |
| `kubeconfig-refresh` | original (optimized 2026-10-17) | pasted kubeconfig YAML, "update my kubeconfig" | `~/.kube/configs/` layout (zshrc glob) |
| `weekly-report` | original (2026-10-17) | "weekly report", "summarize my week" | `draft` + `profiles/reporting`; session history + git + Jira (MCP) at runtime |
| `dotfiles-setup` | original (2026-10-17; pre-flight gate + reset added same day) | "new machine setup", "install dotfiles", "remove and reinstall dotfiles" | Makefile install/clean steps, `scripts/installations/dotfiles.py`, `scripts/skills/` |

## The three sources of a skill at `~/.claude/skills/`

`ls -la ~/.claude/skills/` is the map:

- symlink → this repo's `claude/skills/` — personal, portable
- symlink → the team skills clone under `~/.claude/plugins/` — team repo
  clone (update: `git pull` + re-run its `install.sh`-style links)
- real directory — machine-local (company project tooling that must not
  leave this machine)

## Standby mirrors (leaving-the-team insurance)

`claude/skills-standby/` holds verbatim copies of generic team plugin
skills. They are NOT linked while the plugin exists — the live plugin
serves them and team updates flow automatically. Lifecycle:

- **standby** (zero divergence) → `make skills-sync` fast-forwards the
  mirror to the installed plugin version (run automatically at every
  session start via the settings hook; silent unless something changed)
- **divergence** (you edit a mirror, or upstream changes under your
  local edits) → sync alerts instead of touching it — a promotion
  signal; promote by moving it into `claude/skills/` + `links.conf`
- **plugin gone** (new machine without the marketplace / left the team)
  → `make skills-activate-standby` flips the mirrors into live
  `~/.claude/skills/` symlinks

`.scrubbed` marker: a standby mirror whose company identifiers were
replaced with placeholders (`{TICKET}`, `{JIRA_HOST}`). Sync treats it
as report-only (never fast-forward) and activation skips it unless
`--all` is passed — review it manually first.

## Conventions

- **No personal names** anywhere in content or filenames. No company
  identifiers either — a line enters this repo only if it reads true
  for any engineering team; replace company identifiers with
  placeholders or fictional substitutes.
- **Skill descriptions** are AI-generated functional language (trigger
  words, channel lists), never personal voice; the voice lives in
  `profiles/` only.
- **Channel naming**: message types, never vendor tools (`message` not
  slack, `docs` not wiki, `ticket comment` not Jira comment); `PR` and
  provenance mentions of GitHub/Jira are kept as industry-standard terms.

## Rebuild on a new machine

Run the `dotfiles-setup` skill (`environment/dotfiles-setup/`) — it probes
what is missing and drives these stages with the settings-safety ordering
rules (settings file first, symlink second; never rebuild settings.json):

1. Clone this repo; `make install` (or `make install-dotfiles`) —
   CLAUDE.md, profiles, and personal skills symlinked into `~/.claude/`.
2. Company machine additionally: install the team plugin from the
   marketplace + clone the team skills repo and run its installer
   (team skills + hook-delivered workflow rules). Personal machine:
   `make skills-activate-standby` for the generic standards mirrors.
3. The `skills-sync` SessionStart hook (see `settings/settings.example`)
   keeps standby mirrors current automatically.
