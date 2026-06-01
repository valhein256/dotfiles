# Dotfiles: Add kubectx + align devops verification lists

**Date:** 2026-06-01
**Status:** Design approved, pending implementation

## Problem

`kubectx` and `kubens` (Kubernetes context/namespace switchers) are missing
from the dotfiles install. They ship together via Homebrew's `kubectx`
formula. While auditing where to add them, the devops package list in
`scripts/installations/packages.py` was found to have drifted from the three
verification scripts and the README — `kind`, `grpcurl`, and `vault` exist in
`packages.py` but not in the verification lists.

## Goal

Add `kubectx` (which provides both `kubectx` and `kubens`) to the dotfiles
install, and bring the three verification scripts and the README in sync with
the actual devops package list in `packages.py`.

## Non-goals

- Do not introduce a "single source of truth" for the verification lists
  (e.g., generating them from `packages.py`). That is a separate refactor.
- Do not touch packages outside the devops category.
- Do not install the binaries or run migrations on the user's machine — this
  PR is limited to the repo. The user will run `brew install kubectx` after
  the change lands.

## Approach

1. Add one `Package` entry to `packages.py` for `kubectx`. The Homebrew
   formula installs both `kubectx` and `kubens` binaries in a single install,
   so this is a single package entry.
2. Reorder the existing devops names in the verification scripts and the
   README into a semantic grouping, then add the missing entries (`kind`,
   `grpcurl`, `vault`, `kubectx`).

Final devops order (used everywhere): **kubectl, helm, kind, kubectx,
grpcurl, terraform, terragrunt, vault**.

Grouping rationale:
- k8s tools first: `kubectl, helm, kind, kubectx`
- gRPC tooling: `grpcurl`
- IaC + secrets: `terraform, terragrunt, vault`

## File changes

### `scripts/installations/packages.py`

Insert a new `Package` after the `kubectl` line (currently line 99). The
`kubectx` formula provides both binaries.

```python
            Package("kubectx", PackageManager.BREW, "devops", "kubectx + kubens (Kubernetes context/namespace switcher)"),
```

### `scripts/verifications/post-install-verification.py:72`

Before:
```python
            "kubectl", "helm", "terraform", "terragrunt",  # devops
```

After:
```python
            "kubectl", "helm", "kind", "kubectx", "grpcurl", "terraform", "terragrunt", "vault",  # devops
```

### `scripts/verifications/installation-verification.py:74`

Before:
```python
            "DevOps": ["kubectl", "helm", "terraform", "terragrunt"],
```

After:
```python
            "DevOps": ["kubectl", "helm", "kind", "kubectx", "grpcurl", "terraform", "terragrunt", "vault"],
```

### `scripts/verifications/system-status-checker.py:350`

Before:
```python
            "devops": ["kubectl", "helm", "terraform", "terragrunt"],
```

After:
```python
            "devops": ["kubectl", "helm", "kind", "kubectx", "grpcurl", "terraform", "terragrunt", "vault"],
```

### `README.md:105`

Before:
```markdown
- `devops` - DevOps tools (kubectl, helm, terraform, terragrunt)
```

After:
```markdown
- `devops` - DevOps tools (kubectl, helm, kind, kubectx, grpcurl, terraform, terragrunt, vault)
```

## Files intentionally NOT changed

- `scripts/installations/packages.py` line 99 (kubectl) and following entries
  (helm, kind, grpcurl, terraform, terragrunt, vault) — these stay in their
  current positions; only `kubectx` is inserted between kubectl and helm.

## Commit plan

Two commits, in order:

1. `feat(packages): add kubectx (kubectx + kubens)` — modifies
   `packages.py` only.
2. `chore: align devops package lists in verification scripts and README` —
   modifies the three verification scripts and README.md.

The intermediate state between the two commits is safe: after commit 1 the
verification scripts will not list `kubectx` (or the previously-missing
`kind`/`grpcurl`/`vault`), but verification uses `brew list <name>` against a
hardcoded list — listing fewer items just means fewer checks, not failures.

## Migration

The user runs `brew install kubectx` once after this change lands. There is
no per-machine cleanup or version conflict to handle.

## Testing

### Code-level

1. `kubectx` is loaded as a `BREW` package:
   ```bash
   python3 -c "
   from scripts.installations.packages import LanguagePackageManager, PackageManager
   pm = LanguagePackageManager()
   t = next(p for p in pm.packages if p.name == 'kubectx')
   assert t.manager == PackageManager.BREW
   assert t.category == 'devops'
   print('OK', t.name, t.manager.name, t.category)
   "
   ```

2. `packages.py` devops entries match the three verification lists:
   ```bash
   python3 -c "
   from scripts.installations.packages import LanguagePackageManager
   pm = LanguagePackageManager()
   actual = sorted([p.name for p in pm.packages if p.category == 'devops'])
   expected = sorted(['kubectl', 'helm', 'kind', 'kubectx', 'grpcurl', 'terraform', 'terragrunt', 'vault'])
   assert actual == expected, (actual, expected)
   print('devops aligned:', actual)
   "
   ```

3. The README and three verification scripts share the same ordered list.
   Manual visual check after edits — the implementation plan will list each
   line to verify.

### Install-behavior

After `brew install kubectx`:
```bash
which kubectx kubens             # both should resolve under brew prefix
kubectx --help                   # exits 0
kubens --help                    # exits 0
```

### Out of scope

- Running the full `make install` flow.
- Verifying any other devops package install — they are unchanged by this PR.

## Risks

- **Order drift recurring.** This PR aligns four places (packages.py +
  three verification scripts + README) by hand. Without a single-source-of-
  truth refactor, the next contributor adding a devops package can re-create
  drift. Mitigation: the design doc records the agreed order so future
  additions have a place to slot in.
