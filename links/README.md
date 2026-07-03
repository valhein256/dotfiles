# Symlink manifests

Manifests that tell `scripts/installations/dotfiles.py` which symlinks to
create during `make install`. This is the **single source of truth** for every
link the installer makes — the script has no hardcoded list.

`core.conf` holds all the standard links: core dotfiles (`gitconfig ->
~/.gitconfig`, `zsh/zshrc -> ~/.zshrc`, `tmux -> ~/.tmux`, ...) and the Claude
config (`claude/settings.json -> ~/.claude/settings.json`).

## How it works

- Any file in this directory (except `README.md` and `*.example`) is treated as
  a manifest and read at install time.
- Each non-empty, non-`#` line declares one symlink:

  ```
  <source>    <target>
  ```

  - `<source>` — the source of truth you edit. Two forms:
    - **Repo-relative** (no leading `/`, `~`, or `$`): resolved against the repo
      root, e.g. `claude/settings.json`. Survives moving/cloning the repo.
    - **Absolute / `~` / `$VAR`**: an external file, e.g. `~/Documents/Work/env`.
      Expanded as-is.
  - `<target>` — where the symlink is created (what tools actually read).
    `~` and `$VARS` are expanded.
  - Two whitespace-separated columns.
  - If `<source>` does not exist, that line is warned about and skipped.
  - If `<target>` already exists (real file or old symlink) it is replaced.

## Tracked vs. private manifests

`links/*.conf` are **tracked** — they hold only generic, repo-relative mappings
(no secrets, no machine paths). A manifest that references machine-specific
absolute/external paths or secrets should be named **`*.local.conf`**, which is
gitignored so it stays private while still being picked up at install time.
