---
name: dotfiles-setup
description: Provision this machine from the dotfiles repo in stages — environment (make install steps), the Claude personal layer (settings restore with key-safety ordering, profiles, skills, standby activation), then verification. Fully idempotent; safe to re-run. Use when asked to set up a new machine, install or configure dotfiles, or restore the Claude layer. Triggers: "new machine setup", "install dotfiles", "provision this machine", "新機器設定", "設定新電腦".
---

# Dotfiles setup

Provision a machine from this repo in three stages. Drive the repo's own
tooling (Makefile, scripts/, links.conf) — this skill adds ordering and
safety rules, not new mechanisms. Every stage is idempotent: probe first,
run only what is missing, re-run freely.

## Stage 0 — Probe

Before anything: report machine state, then act only on gaps.

- Repo clean? `git status --porcelain` — uncommitted changes must be
  committed or stashed before Stage 2 touches settings.
- Environment: `command -v brew`, language managers present.
- Claude layer: does `~/.claude/settings.json` resolve (symlink target
  exists)? `./scripts/installations/dotfiles.py --verify` for the whole
  link manifest.
- Report the gap list to the user, then run the missing stages.

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
