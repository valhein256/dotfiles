# Claude Code config

Claude Code config, managed like any other dotfile. The real
`claude/settings/settings.json` holds account-specific values (API key,
enabled plugins, etc.), so it is **gitignored** — only the redacted
`claude/settings/settings.example` and this README are tracked.

`~/.claude/settings.json` is symlinked to `claude/settings/settings.json`
via the `links.conf` line, so editing the repo file takes effect directly
(Claude Code writes settings in place, so `/config` changes also flow back
into this file).

## Setup on a new machine

Ask Claude to run the `dotfiles-setup` skill
(`claude/skills/environment/dotfiles-setup/`) — it drives the full staged
setup with the settings-safety ordering rules.

Manual equivalent, in this order (order matters):

1. Copy a **complete** `settings.json` from your old machine (or a backup)
   to `claude/settings/settings.json` — never rebuild it from the example:
   `apiKeyHelper`, `enabledPlugins`, and env values exist nowhere else.
2. Only then run `make install-dotfiles` (or `make install`) to create the
   symlink.

Writing the API key directly into `~/.claude/settings.json` before linking
loses it: the installer replaces that file with a symlink.

## Local-only files (never committed)

These files live in this repo's tree but are **gitignored** — they carry
machine-specific or work-specific values that must not enter git. They are
the "local config" layer: generated on each machine, passed in via
`links.conf` (or sourced by zsh), restored by copying a complete file from
the old machine when you set up a new machine.

| File | Role | Restore from |
|---|---|---|
| `claude/settings/settings.json` | live Claude Code settings (API key, account values, work marketplace entries) | copy the complete file from the old machine; `claude/settings/settings.example` only fills gaps, with the user supplying `apiKeyHelper` / `enabledPlugins` / env values |
| `claude/settings/settings-*.json` | settings variants for other accounts/providers | copy the complete live file, then edit the provider fields |
| `zsh/local/*.zsh` | per-host PATH tweaks and work-specific env vars | write your own; zshrc sources every `*.zsh` there |

Convention: if a setting needs a value that identifies your employer or any
internal system to work, that value lives ONLY in these local files — the
tracked files (including this README, `settings.example`, and all skills)
use placeholders.
