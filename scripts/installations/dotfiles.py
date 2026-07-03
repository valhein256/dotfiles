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
    
    def create_symlink(self, source: Path, target: Path, description: str) -> None:
        """Create a symbolic link, removing existing file/link if necessary"""
        try:
            # Ensure parent directory exists
            target.parent.mkdir(parents=True, exist_ok=True)
            
            # Remove existing file or symlink
            if target.exists() or target.is_symlink():
                if target.is_symlink():
                    target.unlink()
                else:
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
        """Install every dotfile by creating the symlinks declared in manifests."""
        print("")
        print(f"{Colors.GRAY}#####################################")
        print(f"# scripts/installations/dotfiles.py #")
        print(f"#####################################{Colors.RESET}")
        print("")
        print("### Dotfiles setting...")

        self._link_manifests()

        print("### Dotfiles setting... done !!")
        print("")
        print(f"{Colors.GREEN}# scripts/installations/dotfiles.py Finish !!{Colors.RESET}")
        print("")

    def _manifests_dir(self) -> Path:
        """Directory holding the dotfile symlink manifests."""
        return self.current_path / "links"

    def _read_manifests(self) -> List[Tuple[Path, Path, str]]:
        """Parse links/ manifests into (source, target, description) tuples.

        This is the single source of truth for every symlink the installer
        creates -- core dotfiles and Claude config all live in core.conf, and
        any machine-specific *.local.conf manifests are picked up here too.

        Each manifest is a plain-text file with one "source target" mapping per
        line. Blank lines and lines starting with '#' are ignored. '~' and
        '$VARS' are expanded in both paths. Scaffolding files (.gitkeep,
        README.md, *.example) and hidden files are skipped.

        A source that resolves to a relative path (i.e. does not start with '/',
        '~', or '$VAR') is taken relative to the repo root, so in-repo sources
        can be declared as e.g. `claude/settings.json` without hardcoding the
        repo's absolute location. Absolute and '~'/'$'-anchored sources (files
        outside the repo) keep working as before.
        """
        links_dir = self._manifests_dir()
        mappings: List[Tuple[Path, Path, str]] = []

        if not links_dir.is_dir():
            return mappings

        skip_names = {"README.md"}
        for manifest in sorted(links_dir.iterdir()):
            if (not manifest.is_file()
                    or manifest.name.startswith(".")
                    or manifest.suffix == ".example"
                    or manifest.name in skip_names):
                continue

            for lineno, raw in enumerate(manifest.read_text().splitlines(), 1):
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue

                parts = line.split()
                if len(parts) != 2:
                    self.warning(
                        f"{manifest.name}:{lineno} expected '<source> <target>', "
                        f"skipping: {raw!r}"
                    )
                    continue

                source = Path(os.path.expandvars(parts[0])).expanduser()
                if not source.is_absolute():
                    # Relative source -> resolve against the repo root.
                    source = self.current_path / source
                target = Path(os.path.expandvars(parts[1])).expanduser()
                description = source.name
                mappings.append((source, target, description))

        return mappings

    def _link_manifests(self) -> None:
        """Create every symlink declared in links/ manifests."""
        mappings = self._read_manifests()
        if not mappings:
            self.warning("No symlink manifests found under links/")
            return

        for source, target, description in mappings:
            if not source.exists():
                self.warning(f"Source not found, skipping: {source}")
                continue

            self.info(f"{description} setting...")
            self.create_symlink(source, target, description)

    def verify_installation(self) -> bool:
        """Verify that every symlink declared in the manifests is correct."""
        print("🔍 Verifying dotfiles installation...")

        mappings = self._read_manifests()
        if not mappings:
            self.warning("No symlink manifests found under links/")
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