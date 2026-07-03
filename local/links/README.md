# Symlink manifests

Manifests that tell `scripts/installations/dotfiles.py` which symlinks to
create during `make install`. This is the **single source of truth** for every
link the installer makes — the script has no hardcoded list.

Manifests cover three cases:

1. **Core dotfiles** — `core.conf` (tracked): the standard links like
   `gitconfig -> ~/.gitconfig`, `zsh/zshrc -> ~/.zshrc`, `tmux -> ~/.tmux`.
2. **In-repo local config** — a gitignored payload under `local/` that should
   be symlinked into place, e.g. `local/claude/settings.json` via `claude.conf`.
3. **External / machine-specific files** — config that must live **outside**
   the repo (work paths, secrets, per-host settings), same spirit as
   `zsh/local/*.zsh`.

## How it works

- Any file in this directory (except `.gitkeep`, `README.md`, and `*.example`)
  is treated as a manifest and read at install time.
- Each non-empty, non-`#` line declares one symlink:

  ```
  <source>    <target>
  ```

  - `<source>` — the source of truth you edit. Two forms:
    - **Repo-relative** (no leading `/`, `~`, or `$`): resolved against the repo
      root, e.g. `local/claude/settings.json`. Survives moving/cloning the repo.
    - **Absolute / `~` / `$VAR`**: an external file, e.g.
      `~/Documents/Work/env`. Expanded as-is.
  - `<target>` — where the symlink is created (what tools actually read).
    `~` and `$VARS` are expanded.
  - Two whitespace-separated columns.
  - If `<source>` does not exist, that line is warned about and skipped.
  - If `<target>` already exists (real file or old symlink) it is replaced.

## Tracked vs. local manifests

Manifests are **ignored by default** (`local/links/*` in `.gitignore`), so a
new manifest stays private unless you opt in. A manifest that contains only
generic, repo-relative mappings (no secrets, no machine paths) — like
`claude.conf` — can be tracked by adding a `!local/links/<name>` line to
`.gitignore`. Keep any manifest that references machine-specific absolute paths
or secrets **unlisted** (ignored).

## Example

Copy `claude.example` to a new manifest and edit the paths:

```sh
cp local/links/claude.example local/links/work.conf
$EDITOR local/links/work.conf
```

Then `make install` (or `make install-step-5-dotfiles`) creates the symlinks.
