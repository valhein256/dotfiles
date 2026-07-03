#!/usr/bin/python3
"""
Dotfiles Cleanup Script
Removes the dotfile symlinks declared in links.conf -- the same manifest the
installer reads -- so install and cleanup can never drift out of sync.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


class DotfilesCleanup:
    """Dotfiles cleanup manager"""

    def __init__(self, auto_confirm: bool = False):
        self.auto_confirm = auto_confirm
        self.home = Path.home()
        self.repo_path = Path.cwd()

    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")

    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")

    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ] {message}")

    def remove_file_or_symlink(self, path: Path, description: str) -> None:
        """Safely remove a file, symlink, or directory"""
        if path.exists() or path.is_symlink():
            self.info(f"Removing {description} at {path}")
            try:
                if path.is_dir() and not path.is_symlink():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                self.success(f"{description} removed")
            except Exception as e:
                self.warning(f"Failed to remove {description}: {e}")
        else:
            self.success(f"{description} not found (already clean)")

    def _manifest_file(self) -> Path:
        """The manifest file declaring every dotfile symlink (shared with install)."""
        return self.repo_path / "links.conf"

    def _read_targets(self) -> List[Tuple[Path, str]]:
        """Parse links.conf into (target, description) pairs.

        Mirrors the installer's parser: one "source target" mapping per line,
        blank lines and '#' comments ignored. Cleanup only needs the target
        (the symlink to remove); the source basename is used as a label.
        '~' and '$VARS' in the target are expanded.
        """
        manifest = self._manifest_file()
        targets: List[Tuple[Path, str]] = []

        if not manifest.is_file():
            self.warning(f"links.conf not found at {manifest}")
            return targets

        for lineno, raw in enumerate(manifest.read_text().splitlines(), 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 2:
                self.warning(
                    f"links.conf:{lineno} expected '<source> <target>', "
                    f"skipping: {raw!r}"
                )
                continue

            description = Path(parts[0]).name
            target = Path(os.path.expandvars(parts[1])).expanduser()
            targets.append((target, description))

        return targets

    def show_summary(self, targets: List[Tuple[Path, str]]) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}⚙️  DOTFILES CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove the dotfile symlinks declared in links.conf:")
        print()
        for target, description in targets:
            print(f"  • {target}  ({description})")
        print()
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Original config files in the repository will be preserved")
        print()

    def run_cleanup(self) -> None:
        """Execute dotfiles cleanup"""
        targets = self._read_targets()
        if not targets:
            self.warning("Nothing to clean (no entries in links.conf)")
            return

        self.show_summary(targets)

        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove dotfiles symlinks? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return

        print()
        self.info("Starting dotfiles cleanup...")
        print()

        for target, description in targets:
            self.remove_file_or_symlink(target, description)

        print()
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Dotfiles cleanup complete!")
        print()
        print("All dotfiles symlinks have been removed.")
        print("You can recreate them with: make dotfiles")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Dotfiles Cleanup Script (reads links.conf)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Remove all dotfile symlinks (interactive)
  %(prog)s -y                 # Remove all dotfile symlinks (auto-confirm)
        """
    )

    parser.add_argument('-y', '--yes', action='store_true',
                       help='Auto-confirm cleanup without asking')

    args = parser.parse_args()

    cleanup = DotfilesCleanup(auto_confirm=args.yes)

    try:
        cleanup.run_cleanup()
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
