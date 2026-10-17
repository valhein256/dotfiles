# Claude Code config

Claude Code config, managed like any other dotfile. The real
`claude/settings/settings.json` holds account-specific values (API key,
enabled plugins, etc.), so it is **gitignored** — only the redacted
`claude/settings/settings.example` and this README are tracked.

`~/.claude/settings.json` is symlinked to `claude/settings/settings.json`
via the `links.conf` line, so editing the repo file takes effect directly
(Claude Code writes settings in place, so `/config` changes also flow back
into this file).

## Setup on a new machine (or remove-then-reinstall)

Ask Claude to run the `dotfiles-setup` skill
(`claude/skills/environment/dotfiles-setup/`): it runs the pre-flight
checklist (hard gate — verifies the complete settings.json before
anything moves), hands over the exact commands to run manually, and
verifies afterwards. Password-requiring steps (sudo — e.g. brew cask
upgrades like xquartz) only work in your own terminal, so the
environment install runs manually by design:

    make clean              # remove-then-reinstall only; prompts CLEAN
    make install-dotfiles   # run FIRST after clean — closes the
                            # settings-symlink gap in seconds
    make install            # prompts INSTALL; step 3 may ask the sudo
                            # password for cask upgrades

On a fresh machine, first place a **complete** `settings.json` (copied
from the old machine or a backup) at `claude/settings/settings.json` —
never rebuild it from the example: `apiKeyHelper`, `enabledPlugins`, and
env values exist nowhere else. Claude links (settings, CLAUDE.md,
profiles, personal skills) are created automatically by the link step
from `links.conf` — nothing manual there.

Writing the API key directly into `~/.claude/settings.json` before
linking still loses it from the live position: the installer replaces
that file with a symlink (a non-empty replaced file is backed up to
`backups/` first, and the installer refuses to replace what it cannot
back up — but the repo file remains the source of truth).

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
