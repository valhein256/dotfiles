# Local symlink manifests

Drop-in manifests that tell `scripts/installations/dotfiles.py` to symlink
machine-specific files into place during `make install`.

Use this for config that must live **outside** the repo (work paths, secrets,
per-host settings) but still wants a symlink managed by dotfiles — the same
spirit as `zsh/local/*.zsh`.

## How it works

- Any file in this directory (except `.gitkeep`, `README.md`, and `*.example`)
  is treated as a manifest and read at install time.
- Manifests are **gitignored** — the real machine paths never enter git.
- Each non-empty, non-`#` line declares one symlink:

  ```
  <source>    <target>
  ```

  - `<source>` — the real file on this machine (the source of truth you edit)
  - `<target>` — where the symlink is created (what tools actually read)
  - Two whitespace-separated columns. `~` and `$VARS` are expanded.
  - If `<source>` does not exist, that line is warned about and skipped.
  - If `<target>` already exists (real file or old symlink) it is replaced.

## Example

Copy `claude.example` to `claude.conf` and edit the paths:

```sh
cp local/links/claude.example local/links/claude.conf
$EDITOR local/links/claude.conf
```

Then `make install` (or `make install-step-5-dotfiles`) creates the symlinks.
