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
passes fully. Prefer the Stage 1 manual-execution model for the whole
stretch — the user runs clean + install in their own terminal (TTY for
sudo passwords); the agent may run the removal itself only when no
sudo step is expected, closing the settings gap per rule 2 immediately
after.

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

**Default: the user runs the complete install commands manually in
their own terminal; the agent verifies afterwards.** The agent's shell
and the `!` prefix both run without a TTY, so any step that needs a
sudo password (brew cask pkg installs/upgrades, e.g. xquartz) always
fails in agent-driven runs. The skill's job here is instructions, not
execution: hand the user the complete command list and say which steps
prompt for a password.

Hand the user these commands (remove-then-reinstall runs all three, in
one terminal, back-to-back):

    make clean            # prompts for typed CLEAN
    make install-dotfiles  # seconds — run FIRST after clean: closes
                          # the settings-symlink gap before the long
                          # environment steps (Reset rule 2)
    make install          # prompts for typed INSTALL; step 3 (brew
                          # upgrade) may ask the sudo password for
                          # cask upgrades (xquartz) — enter it when
                          # asked

Order rules (Reset section) still apply in the manual flow: clean →
install in one continuous stretch, no new Claude Code sessions during
the settings-symlink gap, complete settings file in the repo before
the link step runs (Stage 0 already verified it).

Claude links need nothing manual: `make install` step 5
(`install-step-5-dotfiles` → `scripts/installations/dotfiles.py`)
creates every link declared in `links.conf` — settings.json, CLAUDE.md,
the profiles, and the personal skills. An existing regular file at a
target is unlinked and replaced by the symlink (why the API key must
live in the repo file first, never written directly into `~/.claude`).

After the user reports completion: agent-driven follow-ups — `make
skills-sync` (Stage 2, plugin present) and the Stage 3 verification. If
a sudo step still failed in their terminal run, hand back that one
command for a manual re-run and re-verify; never retry a sudo step in
the agent shell.

Agent-driven full `make install` (background, logged) remains possible
when no sudo step is expected — but expect cask-upgrade steps to fail
without a TTY; report and hand the command over instead of retrying.

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
