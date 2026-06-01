# Dotfiles: Switch teleport to official Homebrew formula

**Date:** 2026-06-01
**Status:** Design approved, pending implementation

## Problem

Running `tsh` against the corp cluster fails with:

> Minimum client version supported by the server is 17.0.0-aa but you are using 14.3.3.

The dotfiles install teleport via a custom local Homebrew tap (`local/custom`)
backed by `formulas/teleport.rb`, which pins the version to **v14.3.3**. The
formula will not auto-upgrade, so `brew upgrade` cannot fix this.

## Goal

Switch `teleport` to the official Homebrew formula so it tracks the latest
version (currently 17.x), while preserving the generic `BREW_LOCAL_TAP`
mechanism in `packages.py` for future custom formulas.

## Non-goals

- Do **not** remove `PackageManager.BREW_LOCAL_TAP` or its helper methods
  (`_ensure_local_tap`, `_copy_formula_to_local_tap`,
  `_discover_formula_packages`). The mechanism stays — only its single current
  user (teleport) leaves.
- Do **not** rework the verification scripts: package name `"teleport"` does
  not change, so they keep working.
- Do **not** add a generic "skip auto-discovery if manually defined" guard.
  YAGNI — there are no current collisions; if one shows up later, add it then.

## Approach

1. Change `teleport` in `packages.py` from `BREW_LOCAL_TAP` (with custom formula
   path + local tap) to plain `BREW`. Homebrew's official formula provides
   bottles, so no source build, and version tracks upstream.
2. Delete `formulas/teleport.rb` — no longer needed.
3. Delete the `if package_name == "teleport": continue` special case in
   `_discover_formula_packages()`. Once the formula file is gone, the special
   case is dead code.
4. Update the `README.md` "Custom Formulas" example to use a `<path>`
   placeholder instead of the now-deleted `formulas/teleport.rb`.

The `BREW_LOCAL_TAP` machinery (enum, helpers, Make targets) stays untouched
and remains available for future custom formulas.

## File changes

### `scripts/installations/packages.py`

**1. Lines 118-119 — change manager**

```python
# Before
Package("teleport", PackageManager.BREW_LOCAL_TAP, "network", "Modern SSH server for teams",
       formula_path="formulas/teleport.rb", local_tap_name="local/custom"),

# After
Package("teleport", PackageManager.BREW, "network", "Modern SSH server for teams"),
```

**2. Lines 152-154 — remove teleport skip in `_discover_formula_packages()`**

```python
# Delete these three lines entirely
# Skip teleport as it's manually defined with local tap
if package_name == "teleport":
    continue
```

### `formulas/teleport.rb`

Delete the entire file. Once it's the last file in `formulas/`, the directory
itself disappears from disk (git does not track empty directories).
`_discover_formula_packages()` already guards on `formulas_dir.exists()`, so
this is fine — the next contributor adding a custom formula simply runs
`mkdir formulas && cp <formula>.rb formulas/`.

### `README.md` (lines 223-227)

In the "Custom Formulas" section, replace the second example line:

- Before: `make brew-install-formula FORMULA=formulas/teleport.rb`
- After: `make brew-install-formula FORMULA=<path>       # Install a custom formula`

The `make brew-list-formulas` line above it stays as-is.

## Files intentionally NOT changed

- `scripts/verifications/post-install-verification.py:74` — `"teleport"`
  string in the network category list. Package name is unchanged.
- `scripts/verifications/system-status-checker.py:352` — same.
- `scripts/verifications/installation-verification.py:76` — same.
- `README.md:107` — `network - Network tools (openssh, sshs, teleport)`. Still
  accurate.
- `Makefile` — `brew-install-formula` and `local-taps-*` targets. Still useful
  for future custom formulas.
- `PackageManager.BREW_LOCAL_TAP` enum and helper methods in `packages.py`
  (`_ensure_local_tap`, `_copy_formula_to_local_tap`). Reusable mechanism.

## Migration (run once per machine that has the old version)

The dotfiles install script does not auto-migrate. Run these manually on every
machine currently holding the pinned 14.3.3 build.

### Pre-check

```bash
tsh version              # Expect: Teleport v14.3.3
brew list teleport       # Confirm currently installed
brew tap | grep local    # Expect: local/custom
```

### Remove old version + clean up local tap

```bash
brew uninstall teleport
brew untap local/custom
```

`brew untap local/custom` is safe here because deleting `formulas/teleport.rb`
empties the tap. If you have added other formulas to `local/custom` outside
this PR, skip the `untap` step.

### Install official version

```bash
brew update
brew install teleport
tsh version              # Expect: 17.x
```

### Re-authenticate

```bash
tsh logout
tsh login --proxy=<your-proxy>
```

### When migration is unnecessary

A clean machine running the dotfiles install for the first time will go
straight through the new `BREW` manager — no migration steps needed.

## Testing

### Code-level (verifiable in repo)

1. **Package definition**
   ```bash
   python3 -c "from scripts.installations.packages import LanguagePackageManager; \
              pm = LanguagePackageManager(); \
              print([p for p in pm.packages if p.name == 'teleport'])"
   ```
   Expect: one `Package` with `manager=PackageManager.BREW`, no `formula_path`,
   no `local_tap_name`.

2. **Auto-discovery yields nothing for teleport**
   ```bash
   ls formulas/ 2>/dev/null || echo "formulas/ does not exist (expected)"
   ```
   Expect: either empty output, or the "does not exist" message — git removes
   empty directories when their last file is deleted.

3. **No stray references**
   ```bash
   git grep -n "teleport" -- scripts/ formulas/ README.md Makefile
   ```
   Expect: only the three verification-script entries and `README.md:107`.

### Install-behavior level (after migration)

4. `which tsh` → `/opt/homebrew/bin/tsh` (Apple Silicon) or
   `/usr/local/bin/tsh` (Intel). Not a local tap cellar path.
5. `tsh version` → 17.x.
6. `brew tap | grep local` → no `local/custom`.
7. `brew info teleport` → source is `homebrew/core`.

### Regression checks

8. `python3 scripts/verifications/post-install-verification.py` — teleport row
   should pass (package name unchanged, brew detection still works).
9. `make brew-list-formulas` — should run without error, list nothing
   (`formulas/` is gone or empty).

### Out of scope

The `BREW_LOCAL_TAP` code path is not exercised end-to-end by this change
(nothing currently uses it). The code is left intact; testing it would require
a synthetic formula. Defer until a real formula needs it.

## Risks

- **Migration not applied** — user keeps hitting the v14 incompatibility error
  until they run the migration steps. Mitigation: migration steps are part of
  this design doc and should be referenced in the PR description.
- **Local tap holds other formulas** — if other formulas have been added to
  `local/custom` since this PR was authored, `brew untap local/custom` would
  remove them. Mitigation: pre-check step in migration shows current tap
  contents; the doc warns about it.
