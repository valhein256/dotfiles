# Claude Code config

Claude Code config, managed like any other dotfile. The real `settings.json`
holds account-specific values (AWS profile, etc.), so it is **gitignored** —
only `settings.example` (redacted) and this README are tracked.

`~/.claude/settings.json` is symlinked to `settings.json` here via the
`claude/settings.json` line in `links/core.conf`, so editing this file takes
effect directly (Claude Code writes settings in place, so `/config` changes
also flow back into this file).

## Setup on a new machine

```sh
cp claude/settings.example claude/settings.json
$EDITOR claude/settings.json    # fill in <YOUR_AWS_PROFILE> etc.
```

Then run `make install` (or `make install-step-5-dotfiles`) to create the symlink.
