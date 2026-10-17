---
name: python-uv-deps
description: Personal Python dependency-management rules. Use for ANY Python work — writing/running scripts, adding packages, or creating a project. Enforces uv-only, per-project .venv, never global pip. Layers on top of team-python-standards.
user_invocable: false
---

# Python Dependency Management (Personal — uv only)

## Precedence

This skill is **additive** on top of `team-python-standards`.

- `team-python-standards` remains in full force for code structure
  (Protocol/ABC service layer, Pydantic settings, pytest, structlog,
  error handling, type hints, secrets handling).
- This skill **only adds rules or makes them stricter** for *dependency
  management and environment setup*. It never relaxes a team rule.
- On any conflict, follow the **stricter** rule.

## Why uv-only (machine facts)

This machine has a specific, deliberate setup — respect it:

- `python3` resolves to **uv-managed CPython** (`~/.local/share/uv/shims/python3`).
- The global interpreter is **PEP 668 externally-managed** — a bare
  `pip install` into it **fails by design**. Do not try to work around it.
- There is **no pyenv / conda / asdf**. `uv` is the only version & env manager.
- System Python (`/usr/bin/python3`, 3.9.6) is off-limits.

## Hard Rules

1. **uv is the only tool.** Never `pip install` into the global/system
   interpreter. Never `python -m venv` by hand. Never `conda`, `pipenv`,
   or `poetry`.
2. **Every project gets its own `.venv`** created and managed by uv.
   No shared/global package installs, ever.
3. **Declare dependencies, don't ad-hoc install.** Use `uv add` so the
   package is recorded in `pyproject.toml` and pinned in `uv.lock`.
4. **`uv.lock` is committed** to version control for reproducibility.
5. **Run via `uv run`** — never rely on a manually-activated venv or a
   globally-resolved `python`. `uv run` guarantees the project `.venv`.
6. **Pin a Python version** per project with `.python-version` (via
   `uv python pin`) so the env is reproducible.

## When a package is missing during development

Do this, in this order — never fall back to global pip:

```bash
# 1. Make sure you're in the project root (has or will have pyproject.toml)
cd <project-root>

# 2. First time only: initialize the project (creates pyproject.toml,
#    .python-version, .venv, uv.lock)
uv init                  # for an application/script project
uv python pin 3.14       # pin interpreter (adjust version as needed)

# 3. Add the missing package — records it in pyproject.toml + uv.lock
uv add <package>         # runtime dependency
uv add --dev <package>   # dev/test-only (pytest, ruff, mypy, ...)

# 4. Run the code through uv (auto-uses the project .venv)
uv run python <script>.py
uv run pytest
```

## If uv is NOT installed

Never assume uv exists. Check first; never silently fall back to global pip.

```bash
command -v uv    # no output → uv is not installed
```

When uv is missing, follow this order — **do not** route around it:

1. **Stop and report.** Tell the user uv is absent. Do NOT silently
   substitute `pip install`, `python -m venv`, poetry, or conda.
2. **Propose installing uv** (don't auto-run — installing a system tool is
   an outward/hard-to-reverse action, so confirm first):
   ```bash
   brew install uv                                   # preferred on this machine (Homebrew)
   # or: curl -LsSf https://astral.sh/uv/install.sh | sh   # official installer
   ```
   uv is a standalone binary — installing it does **not** touch or pollute
   any Python environment.
3. **Only if uv genuinely cannot be installed** (locked-down/restricted
   host) consider a fallback — and only a **project-isolated** one:
   `python -m venv .venv` + that venv's pip. Never the global/system
   interpreter.
4. **Never degrade silently.** Any deviation from uv-only MUST be announced
   to the user with the reason, before proceeding — not buried in a command.

## Quick Reference

| Need | Command | Never |
|------|---------|-------|
| New project | `uv init` + `uv python pin <ver>` | `python -m venv` |
| Add runtime dep | `uv add <pkg>` | `pip install <pkg>` |
| Add dev/test dep | `uv add --dev <pkg>` | global pip |
| Install one-off tool | `uv tool install <tool>` | global pip |
| Run a script | `uv run python x.py` | `python x.py` |
| Run tests | `uv run pytest` | `pytest` (bare) |
| Sync env to lock | `uv sync` | manual pip install |
| Reproducible env | commit `uv.lock` + `.python-version` | unpinned deps |

## Checklist (dependency-management review)

- [ ] uv presence checked (`command -v uv`); if absent, reported — not worked around
- [ ] No bare `pip install` / `python -m venv` / poetry / conda anywhere
- [ ] Project has `pyproject.toml`, `uv.lock`, and `.python-version`
- [ ] All deps added via `uv add` (runtime) / `uv add --dev` (dev)
- [ ] `uv.lock` is committed
- [ ] Scripts/tests invoked with `uv run`
- [ ] No global/system-interpreter package installs
