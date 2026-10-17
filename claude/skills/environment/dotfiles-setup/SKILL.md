---
name: dotfiles-setup
description: Provision this machine from the dotfiles repo in stages — pre-flight checklist (hard gate), optional reset (remove the repo-managed setup), environment (make install steps), the Claude personal layer (settings restore with key-safety ordering, profiles, skills, standby activation), then verification. Fully idempotent; safe to re-run. Use when asked to set up a new machine, install or configure dotfiles, remove and reinstall, or restore the Claude layer. Triggers: "new machine setup", "install dotfiles", "provision this machine", "remove and reinstall dotfiles".
---

# Dotfiles setup

Provision a machine from this repo in stages. Drive the repo's own
tooling (Makefile, scripts/, links.conf) — this skill adds ordering and
safety rules, not new mechanisms. Every stage is idempotent: pre-flight
first, run only what is missing, re-run freely.

## Stage 0 — Pre-flight checklist (hard gate)

Run EVERY check, print the full table, and STOP before any removal or
setup step unless every REQUIRED row passes. Never print secret values —
field presence only.

| # | Item | Verify | Required |
|---|---|---|---|
| 1 | settings.json complete | `claude/settings/settings.json` exists and contains `apiKeyHelper`, `enabledPlugins` (>=1), `env.ANTHROPIC_BASE_URL`, `hooks.SessionStart` | YES — hard stop |
| 2 | Variants complete | each `claude/settings/settings-*.json` has `enabledPlugins`; `fw-*` variants also `apiKeyHelper` | warn only |
| 3 | Repo clean | `git status --porcelain` empty (commit or stash first) | YES — hard stop |
| 4 | No other Claude sessions | ask the user; `ps` for other claude processes | YES — hard stop |
| 5 | CLT tools alive | `/usr/bin/python3`, `/usr/bin/make`, `/usr/bin/git` exist | YES (reset path) |
| 6 | Local layer present | `zsh/local/*.zsh`, `claude/settings/settings.example` exist | warn only |
| 7 | Team plugin state | `~/.claude/plugins` has the team plugin → Stage 2 runs `make skills-sync`; absent → `make skills-activate-standby` | report |
| 8 | Level-2 assets | real-dir skills under `~/.claude/skills` + `~/.claude/projects` memory backed up | YES only if wiping `~/.claude` |

On any REQUIRED fail: name the missing asset and stop — never enter
removal or setup with incomplete assets.

After the gate passes: report the gap list (what is missing → which
stages run), then run only the missing stages.

## Reset (optional — remove the repo-managed setup)

Run only when the goal is remove-then-reinstall, and only after Stage 0
passes fully.

Removal: `make clean` (prompts for typed `CLEAN`) or the individual
`make clean-step-N-*` targets. It removes brew packages/taps, language
managers, neovim dynamic content, every links.conf symlink, git
submodules, and caches. Real files survive: the local layer
(`claude/settings/*.json`, `zsh/local/*.zsh`) is untouched.

Order rules:

1. **Clean and reinstall in one continuous stretch** — never leave the
   settings symlink dangling across sessions or overnight.
2. **Close the settings gap first**: right after clean finishes, run
   the link step (`make install-dotfiles`) before the long environment
   steps. The repo settings file is already in place (Stage 0 checked
   it); linking takes seconds and ends the dangling window.
3. **No new Claude Code sessions between clean and relink** — a fresh
   session reads no settings, and its first settings save writes a
   defaults-only file (no `apiKeyHelper` — unreconstructable).
4. **Level 2 (wiping `~/.claude` entirely) is a separate manual
   decision**: back up the one-copy assets first (Stage 0 row 8) —
   `make clean` never touches them, but a wipe destroys them
   permanently.

## Stage 1 — Environment

Run the repo's existing steps in order:

    make install-step-1-local-taps ... install-step-7-neovim

(or `make install` — it prompts for typed confirmation `INSTALL`.)

- Long-running (brew). Steps continue on failure — collect every failure
  and report them; never silently retry.

## Stage 2 — Claude personal layer (safety-critical)

### Settings restore — hard rules

1. **Never rebuild settings.json from settings.example or from memory.**
   Machine-local fields (`apiKeyHelper`, `enabledPlugins`, env values,
   hooks) exist nowhere except a complete settings.json. Restore by
   copying a complete file (old machine, backup, or user-pasted content)
   — never by assembling one.
2. **Order: file first, link second.** Place the complete settings.json
   at `claude/settings/settings.json` (machine-local, gitignored — never
   committed), THEN run the link step (`make install-dotfiles`). Never
   put the API key directly in `~/.claude/settings.json` before linking:
   the installer unlinks an existing regular file there and replaces it
   with a symlink, destroying its content.
3. **No dangling-symlink windows.** Any move of a settings file and the
   symlink re-point run in the same shell command.
4. **No clobber.** Never `mv`/`cp` over a settings file without reading
   both sides and diffing first.
5. **Edit the repo path, never the symlink path.**
6. **Degradation** (no complete file available): start from
   `claude/settings/settings.example`, then list the missing fields
   explicitly (`apiKeyHelper`, `enabledPlugins`, env values, hooks) and
   get each from the user. State that plugins stay disabled until
   `enabledPlugins` is filled.

### Provider variants

`claude/settings/settings-*.json` switch providers. Variants are created
only by copying a complete live file, never from the example. Switching:
save the live file into its variant, then copy the target variant over
the live file — both copies, rule 4 applies.

### Profiles and skills

- `claude/CLAUDE.md`, `profiles/`, and the personal skills are tracked —
  the link step covers them; verify with `--verify`.
- Team plugin missing (`~/.claude/plugins` without it): `make
  skills-activate-standby` flips the standby mirrors into live skills.
  Plugin installed: `make skills-sync` fast-forwards the mirrors.

## Stage 3 — Verify and report

- `./scripts/installations/dotfiles.py --verify`
- `git check-ignore claude/settings/settings.json` must succeed.
- `readlink ~/.claude/settings.json` resolves; `apiKeyHelper` and
  `enabledPlugins` present in the resolved file.
- Report: what ran, what failed, what still needs the user (API key,
  plugin installs, manual steps).

## Never

- Commit or push anything under `claude/settings/` except
  `settings.example`.
- Write the API key into any tracked file, message, or log.
