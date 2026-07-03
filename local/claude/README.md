# Local Claude config

Machine-local Claude Code config. The real `settings.json` here holds
account-specific values (AWS profile, etc.), so it is **gitignored** — only
`settings.example` (redacted) and this README are tracked.

`~/.claude/settings.json` is symlinked to `settings.json` here via the
`local/links/claude.conf` manifest, so editing this file takes effect directly.

## Setup on a new machine

```sh
cp local/claude/settings.example local/claude/settings.json
$EDITOR local/claude/settings.json    # fill in <YOUR_AWS_PROFILE> etc.
```

Then ensure `local/links/claude.conf` contains:

```
~/Documents/dotfiles/local/claude/settings.json    ~/.claude/settings.json
```

and run `make install` (or `make install-step-5-dotfiles`) to create the symlink.
