#!/usr/bin/env python3
"""External Plugin Manager (formerly git-submodule.py).

Despite the filename — kept for Makefile compatibility — this no longer
manages git submodules. zplug and tpm used to be pinned via .gitmodules,
but that broke as soon as zplug renamed its default branch (master -> main),
and we didn't actually want a pinned version anyway.

This script now treats them as plain external clones:
  * if the working tree is missing, clone it shallow
  * if it exists, fast-forward to the upstream default branch
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'
    RESET = '\033[0m'


# (url, working-tree path relative to dotfiles root)
PLUGINS: List[Tuple[str, str]] = [
    ("https://github.com/zplug/zplug",       "zsh/zplug"),
    ("https://github.com/tmux-plugins/tpm",  "tmux/plugins/tpm"),
]


def info(msg: str) -> None:
    print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {msg}")


def ok(msg: str) -> None:
    print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {msg}")


def warn(msg: str) -> None:
    print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ] {msg}")


def fail(msg: str) -> None:
    print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {msg}")


def run(cmd: List[str], cwd: Path) -> int:
    """Run a command streaming output. Return exit code."""
    info("Running: " + " ".join(cmd))
    try:
        result = subprocess.run(cmd, cwd=cwd, check=False)
        return result.returncode
    except FileNotFoundError as e:
        fail(f"Command not found: {e}")
        return 127


def clone_or_update(url: str, path: Path, repo_root: Path) -> bool:
    """Clone the plugin if missing, otherwise pull --ff-only against its
    current upstream branch (whatever HEAD is tracking).

    Returns True on success, False if the plugin ended up not usable.
    """
    target = repo_root / path
    git_dir = target / ".git"

    if not git_dir.exists():
        info(f"{path}: clone from {url}")
        target.parent.mkdir(parents=True, exist_ok=True)
        rc = run(["git", "clone", "--depth=1", url, str(target)], cwd=repo_root)
        if rc != 0:
            fail(f"{path}: clone failed (exit {rc})")
            return False
        ok(f"{path}: cloned")
        return True

    # Existing checkout — fast-forward to upstream.
    # `git pull --ff-only` against the configured upstream branch handles the
    # zplug rename case automatically: the local branch tracks whatever the
    # clone created, and pulling against that ref doesn't care about
    # 'master' vs 'main'.
    info(f"{path}: fast-forward to upstream")
    rc = run(["git", "-C", str(target), "pull", "--ff-only"], cwd=repo_root)
    if rc != 0:
        warn(f"{path}: pull --ff-only failed (exit {rc}); leaving working tree alone")
        return False
    ok(f"{path}: up to date")
    return True


def find_dotfiles_root() -> Path:
    """Resolve the dotfiles repo root regardless of where the script was run from."""
    here = Path(__file__).resolve()
    # scripts/installations/git-submodule.py -> dotfiles/
    return here.parent.parent.parent


def main() -> int:
    # CLI flags retained for compatibility with the old script.
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("External Plugin Manager")
        print("Usage:")
        print("  git-submodule.py            # Clone or fast-forward each plugin")
        print("  git-submodule.py --status   # Show status of each plugin")
        print("  git-submodule.py --verify   # Exit non-zero if any plugin is missing")
        return 0

    repo_root = find_dotfiles_root()

    if len(sys.argv) > 1 and sys.argv[1] == "--status":
        print("Plugin status:")
        for url, path in PLUGINS:
            target = repo_root / path
            if (target / ".git").exists():
                try:
                    head = subprocess.check_output(
                        ["git", "-C", str(target), "rev-parse", "--short", "HEAD"],
                        text=True,
                    ).strip()
                    print(f"  {path:<25} @ {head}  ({url})")
                except subprocess.CalledProcessError:
                    print(f"  {path:<25} @ <unreadable>  ({url})")
            else:
                print(f"  {path:<25} <missing>  ({url})")
        return 0

    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        missing = [p for _, p in PLUGINS if not (repo_root / p / ".git").exists()]
        if missing:
            for p in missing:
                fail(f"missing plugin: {p}")
            return 1
        ok("All plugins present")
        return 0

    print("")
    print(f"{Colors.GRAY}##########################################")
    print("# scripts/installations/git-submodule.py #")
    print(f"##########################################{Colors.RESET}")
    print("")
    print("### External plugin clone/update...")

    all_ok = True
    for url, path in PLUGINS:
        if not clone_or_update(url, Path(path), repo_root):
            all_ok = False

    print("### External plugin clone/update... done !!")
    print("")
    if all_ok:
        print(f"{Colors.GREEN}# scripts/installations/git-submodule.py Finish !!{Colors.RESET}")
        return 0
    else:
        warn("Some plugins failed; review messages above")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print()
        fail("Cancelled by user")
        sys.exit(1)
