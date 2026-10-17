# Claude Code config

Claude Code config, managed like any other dotfile. The real `settings.json`
holds account-specific values (AWS profile, etc.), so it is **gitignored** —
only `settings.example` (redacted) and this README are tracked.

`~/.claude/settings.json` is symlinked to `settings.json` here via the
`claude/settings.json` line in `links.conf`, so editing this file takes effect
directly (Claude Code writes settings in place, so `/config` changes also flow
back into this file).

## Setup on a new machine

```sh
cp claude/settings.example claude/settings.json
$EDITOR claude/settings.json    # fill in <YOUR_AWS_PROFILE> etc.
```

Then run `make install` (or `make install-step-5-dotfiles`) to create the symlink.

## Local-only files (never committed)

These files live in this repo's tree but are **gitignored** — they carry
machine-specific or work-specific values that must not enter git. They are
the "local config" layer: generated on each machine, passed in via
`links.conf` (or sourced by zsh), rebuilt by hand from the tracked example
when you set up a new machine.

| File | Role | Rebuild from |
|---|---|---|
| `claude/settings.json` | live Claude Code settings (account values, work marketplace entries) | `claude/settings.example` + your values |
| `claude/settings-*.json` | settings variants for other accounts/providers | same, per variant |
| `zsh/local/*.zsh` | per-host PATH tweaks and work-specific env vars | write your own; zshrc sources every `*.zsh` there |

Convention: if a setting needs a value that identifies your employer or any
internal system to work, that value lives ONLY in these local files — the
tracked files (including this README, `settings.example`, and all skills)
use placeholders.
