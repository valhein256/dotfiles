#!/usr/bin/env python3
"""
Dotfiles Installation Script
Creates symbolic links for all dotfiles and configurations.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'


class DotfilesInstaller:
    """Dotfiles installation manager"""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.home = Path.home()
        self.platform = os.uname().sysname
    
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def fail(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
        print("")
        sys.exit(1)
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ] {message}")
    
    def _backup_replaced_target(self, target: Path) -> bool:
        """Back up a real file/dir that a symlink is about to replace.

        Deleting silently is how machine-local data (API keys, plugin
        state) has been lost before: an existing regular file at a
        target was unlinked with no warning and no copy. Guard: any
        non-empty file (or any directory) leaves a dated copy under
        backups/ first. Empty files are deleted as before. A failed
        backup aborts the replacement (returns False) — never destroy
        what could not be copied.
        """
        import shutil
        import time

        if target.is_file() and target.stat().st_size == 0:
            return True  # nothing to lose

        backup_dir = self.current_path / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d-%H%M%S")
        backup = backup_dir / f"{target.name}.bak-{stamp}"
        try:
            if target.is_dir():
                shutil.copytree(target, backup)
            else:
                shutil.copy2(target, backup)
        except Exception as e:
            self.fail(
                f"Refusing to replace {target}: backup failed ({e}) — "
                f"resolve manually before re-running"
            )
            return False

        self.warning(
            f"replaced real file at {target} — backup: {backup}"
        )
        return True

    def create_symlink(self, source: Path, target: Path, description: str) -> None:
        """Create a symbolic link, backing up any real file/dir it replaces"""
        try:
            # Ensure parent directory exists
            target.parent.mkdir(parents=True, exist_ok=True)

            # Remove existing file or symlink (real content is backed up first)
            if target.exists() or target.is_symlink():
                if target.is_symlink():
                    target.unlink()
                else:
                    if not self._backup_replaced_target(target):
                        return  # backup failed and already reported; keep target
                    if target.is_dir():
                        import shutil
                        shutil.rmtree(target)
                    else:
                        target.unlink()

            # Create symlink
            target.symlink_to(source)
            self.success(f"{description} symlinked")

        except Exception as e:
            self.fail(f"Failed to create symlink for {description}: {e}")
    
    def install_dotfiles(self) -> None:
        """Install every dotfile by creating the symlinks declared in links.conf."""
        print("")
        print(f"{Colors.GRAY}#####################################")
        print(f"# scripts/installations/dotfiles.py #")
        print(f"#####################################{Colors.RESET}")
        print("")
        print("### Dotfiles setting...")

        self._link_manifest()

        print("### Dotfiles setting... done !!")
        print("")
        print(f"{Colors.GREEN}# scripts/installations/dotfiles.py Finish !!{Colors.RESET}")
        print("")

    def _manifest_file(self) -> Path:
        """The manifest file declaring every dotfile symlink."""
        return self.current_path / "links.conf"

    def _read_manifest(self) -> List[Tuple[Path, Path, str]]:
        """Parse links.conf into (source, target, description) tuples.

        This is the single source of truth for every symlink the installer
        creates -- core dotfiles and Claude config alike.

        The file has one "source target" mapping per line. Blank lines and
        lines starting with '#' are ignored. '~' and '$VARS' are expanded in
        both paths.

        A source that resolves to a relative path (i.e. does not start with '/',
        '~', or '$VAR') is taken relative to the repo root, so in-repo sources
        can be declared as e.g. `claude/settings.json` without hardcoding the
        repo's absolute location. Absolute and '~'/'$'-anchored sources (files
        outside the repo) keep working as before.
        """
        manifest = self._manifest_file()
        mappings: List[Tuple[Path, Path, str]] = []

        if not manifest.is_file():
            return mappings

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

            source = Path(os.path.expandvars(parts[0])).expanduser()
            if not source.is_absolute():
                # Relative source -> resolve against the repo root.
                source = self.current_path / source
            target = Path(os.path.expandvars(parts[1])).expanduser()
            mappings.append((source, target, source.name))

        return mappings

    def _link_manifest(self) -> None:
        """Create every symlink declared in links.conf."""
        mappings = self._read_manifest()
        if not mappings:
            self.warning("No symlinks found in links.conf")
            return

        for source, target, description in mappings:
            if not source.exists():
                self.warning(f"Source not found, skipping: {source}")
                continue

            self.info(f"{description} setting...")
            self.create_symlink(source, target, description)

    def verify_installation(self) -> bool:
        """Verify that every symlink declared in links.conf is correct."""
        print("🔍 Verifying dotfiles installation...")

        mappings = self._read_manifest()
        if not mappings:
            self.warning("No symlinks found in links.conf")
            return False

        all_good = True
        for source, target, description in mappings:
            if target.is_symlink() and target.exists():
                self.success(f"{description} correctly linked")
            else:
                self.warning(f"{description} not properly linked")
                all_good = False

        return all_good


def main():
    """Main function"""
    installer = DotfilesInstaller()
    
    try:
        installer.install_dotfiles()
        
        # Optional verification
        if len(sys.argv) > 1 and sys.argv[1] == "--verify":
            installer.verify_installation()
            
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()