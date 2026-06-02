#!/usr/bin/python3
"""
Language Managers Cleanup Script
Removes all language version managers and their installations.
"""

import argparse
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import List, Dict


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


class LanguageManagersCleanup:
    """Language managers cleanup manager"""
    
    def __init__(self, auto_confirm: bool = False):
        self.auto_confirm = auto_confirm
        self.home = Path.home()
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def remove_directory(self, path: Path, description: str) -> None:
        """Safely remove a directory and all its contents"""
        if path.exists():
            self.info(f"Removing {description} at {path}")
            try:
                # First try normal removal
                shutil.rmtree(path)
                self.success(f"{description} removed")
            except (PermissionError, OSError) as e:
                try:
                    # If permission denied, try to fix permissions first
                    import subprocess
                    subprocess.run(['chmod', '-R', 'u+w', str(path)], check=False, capture_output=True)
                    shutil.rmtree(path)
                    self.success(f"{description} removed (with permission fix)")
                except Exception as e2:
                    self.warning(f"Failed to remove {description}: {e2}")
            except Exception as e:
                self.warning(f"Failed to remove {description}: {e}")
        else:
            self.success(f"{description} not found (already clean)")
    
    def remove_symlinks_pointing_into(self, link_dir: Path, target_root: Path, description: str) -> None:
        """Remove symlinks in link_dir whose target is under target_root.

        Catches both live and broken symlinks (readlink works on broken ones too).
        Without this, `uv tool install` later refuses to overwrite the leftover
        link with "Executable already exists".
        """
        if not link_dir.is_dir():
            self.success(f"{description} skipped (no {link_dir})")
            return
        target_root_str = str(target_root.resolve() if target_root.exists() else target_root)
        removed = 0
        for entry in link_dir.iterdir():
            if not entry.is_symlink():
                continue
            try:
                link_target = os.readlink(entry)
            except OSError:
                continue
            if not link_target.startswith(target_root_str) and not link_target.startswith(str(target_root)):
                continue
            try:
                entry.unlink()
                removed += 1
            except OSError as e:
                self.warning(f"Failed to remove symlink {entry}: {e}")
        if removed:
            self.success(f"{description}: removed {removed} symlink(s) from {link_dir}")
        else:
            self.success(f"{description}: no matching symlinks in {link_dir}")

    def remove_broken_symlinks(self, link_dir: Path, description: str) -> None:
        """Remove broken (dangling) symlinks in link_dir as a final sweep."""
        if not link_dir.is_dir():
            return
        removed = 0
        for entry in link_dir.iterdir():
            if entry.is_symlink() and not entry.exists():
                try:
                    entry.unlink()
                    removed += 1
                except OSError as e:
                    self.warning(f"Failed to remove broken symlink {entry}: {e}")
        if removed:
            self.success(f"{description}: removed {removed} broken symlink(s) from {link_dir}")
        else:
            self.success(f"{description}: no broken symlinks in {link_dir}")

    def cleanup_python_uv(self) -> None:
        """Remove uv and all Python installations"""
        print(f"\n🐍 Python (uv) Cleanup")

        directories = [
            (self.home / ".local" / "share" / "uv", "uv data directory"),
            (self.home / ".cache" / "uv", "uv cache"),
            (self.home / ".config" / "uv", "uv config"),
        ]

        for path, description in directories:
            self.remove_directory(path, description)

        # uv tool install creates symlinks in ~/.local/bin pointing into
        # ~/.local/share/uv/. Removing the share dir alone leaves them as
        # broken links, and a later `uv tool install` will refuse to
        # overwrite them. Sweep them out by target.
        self.remove_symlinks_pointing_into(
            self.home / ".local" / "bin",
            self.home / ".local" / "share" / "uv",
            "uv-installed binaries"
        )

    def cleanup_pipx(self) -> None:
        """Remove pipx environments and any symlinks it created."""
        print(f"\n📦 pipx Cleanup")

        self.remove_directory(self.home / ".local" / "pipx", "pipx data directory")
        self.remove_symlinks_pointing_into(
            self.home / ".local" / "bin",
            self.home / ".local" / "pipx",
            "pipx-installed binaries"
        )
    
    def cleanup_nodejs_fnm(self) -> None:
        """Remove fnm and all Node.js installations"""
        print(f"\n🟢 Node.js (fnm) Cleanup")
        
        directories = [
            (self.home / ".local" / "share" / "fnm", "fnm data directory"),
            (self.home / ".cache" / "fnm", "fnm cache"),
            (self.home / ".fnm", "fnm alternative location"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_java_sdkman(self) -> None:
        """Remove SDKMAN and all Java installations"""
        print(f"\n☕ Java (SDKMAN) Cleanup")
        
        directories = [
            (self.home / ".sdkman", "SDKMAN installation (includes all JDKs, Maven, Gradle)"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_rust_rustup(self) -> None:
        """Remove rustup and all Rust installations"""
        print(f"\n🦀 Rust Cleanup")
        
        directories = [
            (self.home / ".rustup", "rustup toolchain directory"),
            (self.home / ".cargo", "cargo packages directory"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_go_environment(self) -> None:
        """Remove Go workspace and caches"""
        print(f"\n🔵 Go Cleanup")
        
        directories = [
            (self.home / "go", "Go workspace (GOPATH)"),
            (self.home / ".cache" / "go-build", "Go build cache"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_legacy_managers(self) -> None:
        """Remove legacy language managers"""
        print(f"\n🗂️  Legacy Managers Cleanup")
        
        directories = [
            (self.home / ".pyenv", "legacy Python (pyenv)"),
            (self.home / ".nvm", "legacy Node.js (nvm)"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_language_caches(self) -> None:
        """Remove language-specific caches"""
        print(f"\n🗑️  Language Caches Cleanup")
        
        directories = [
            # Python caches
            (self.home / ".cache" / "pip", "Python pip cache"),
            (self.home / ".cache" / "poetry", "Python poetry cache"),
            (self.home / ".cache" / "pipenv", "Python pipenv cache"),
            # Node.js caches
            (self.home / ".npm", "Node.js npm cache"),
            (self.home / ".cache" / "yarn", "Node.js yarn cache"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def get_cleanup_summary(self) -> Dict[str, List[str]]:
        """Get summary of what will be cleaned"""
        return {
            "Python (uv)": [
                "~/.local/share/uv (all Python versions)",
                "~/.cache/uv (cache)",
                "~/.config/uv (config)",
                "~/.local/bin/* symlinks pointing into ~/.local/share/uv"
            ],
            "pipx": [
                "~/.local/pipx (all pipx-installed venvs)",
                "~/.local/bin/* symlinks pointing into ~/.local/pipx"
            ],
            "Node.js (fnm)": [
                "~/.local/share/fnm (all Node versions)",
                "~/.cache/fnm (cache)",
                "~/.fnm (alternative location)"
            ],
            "Java (SDKMAN)": [
                "~/.sdkman (all JDKs, Maven, Gradle)"
            ],
            "Rust": [
                "~/.rustup (all toolchains)",
                "~/.cargo (all packages)"
            ],
            "Go": [
                "~/go (workspace)",
                "~/.cache/go-build (build cache)"
            ],
            "Legacy": [
                "~/.pyenv (old Python manager)",
                "~/.nvm (old Node.js manager)"
            ],
            "Caches": [
                "~/.cache/pip, ~/.cache/poetry, ~/.cache/pipenv",
                "~/.npm, ~/.cache/yarn"
            ]
        }
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}🔧 LANGUAGE MANAGERS CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove ALL language managers and their data:")
        print()
        
        summary = self.get_cleanup_summary()
        for category, items in summary.items():
            print(f"📂 {category}:")
            for item in items:
                print(f"  • {item}")
            print()
        
        print(f"{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]WARNING: This will remove ALL language installations and packages!{Colors.RESET}")
        print()
    
    def run_cleanup(self) -> None:
        """Execute language managers cleanup"""
        self.show_summary()
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove all language managers? Type 'CLEANUP' to confirm: ")
            if confirmation != "CLEANUP":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting language managers cleanup...")
        
        # Execute cleanup for each language
        self.cleanup_python_uv()
        self.cleanup_pipx()
        self.cleanup_nodejs_fnm()
        self.cleanup_java_sdkman()
        self.cleanup_rust_rustup()
        self.cleanup_go_environment()
        self.cleanup_legacy_managers()
        self.cleanup_language_caches()

        # Final sweep: any other broken symlinks in ~/.local/bin
        # (e.g. left by previous tooling we don't track explicitly).
        print(f"\n🧹 Final symlink sweep")
        self.remove_broken_symlinks(self.home / ".local" / "bin", "broken symlinks")
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Language managers cleanup complete!{Colors.RESET}")
        print()
        print("All language version managers and their installations have been removed.")
        print("You can reinstall with: make language-managers")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Language Managers Cleanup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Interactive mode with confirmation
  %(prog)s -y                 # Auto-confirm cleanup
        """
    )
    
    parser.add_argument('-y', '--yes', action='store_true',
                       help='Auto-confirm cleanup without asking')
    
    args = parser.parse_args()
    
    cleanup = LanguageManagersCleanup(auto_confirm=args.yes)
    
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