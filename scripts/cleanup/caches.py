#!/usr/bin/env python3
"""
Caches Cleanup Script
Removes various development-related caches and temporary files.
"""

import argparse
import shutil
import subprocess
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


class CachesCleanup:
    """Caches cleanup manager"""
    
    def __init__(self, auto_confirm: bool = False):
        self.auto_confirm = auto_confirm
        self.home = Path.home()
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def run_command(self, cmd: str, capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def remove_directory(self, path: Path, description: str) -> None:
        """Safely remove a directory and all its contents"""
        if path.exists():
            # Get size before removal for reporting
            try:
                size = sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
                size_mb = size / (1024 * 1024)
                self.info(f"Removing {description} at {path} ({size_mb:.1f}MB)")
            except:
                self.info(f"Removing {description} at {path}")
            
            try:
                shutil.rmtree(path)
                self.success(f"{description} removed")
            except Exception as e:
                self.warning(f"Failed to remove {description}: {e}")
        else:
            self.success(f"{description} not found (already clean)")
    
    def cleanup_homebrew_caches(self) -> None:
        """Remove Homebrew caches"""
        print(f"\n🍺 Homebrew Caches Cleanup")
        
        cache_dirs = [
            (self.home / "Library" / "Caches" / "Homebrew", "Homebrew cache"),
            (self.home / "Library" / "Logs" / "Homebrew", "Homebrew logs"),
        ]
        
        for path, description in cache_dirs:
            self.remove_directory(path, description)
        
        # Run brew cleanup
        self.info("Running brew cleanup --prune=all...")
        result = self.run_command("brew cleanup --prune=all", capture_output=False)
        if result and result.returncode == 0:
            self.success("Brew cleanup completed")
        else:
            self.warning("Brew cleanup may have failed")
        
        # Remove Homebrew cache again after brew cleanup to ensure it's completely clean
        homebrew_cache = self.home / "Library" / "Caches" / "Homebrew"
        if homebrew_cache.exists():
            self.info("Removing Homebrew cache again (post-cleanup)")
            self.remove_directory(homebrew_cache, "Homebrew cache (final cleanup)")
    
    def cleanup_language_caches(self) -> None:
        """Remove language-specific caches"""
        print(f"\n🔧 Language Caches Cleanup")
        
        cache_dirs = [
            # Python caches
            (self.home / ".cache" / "pip", "Python pip cache"),
            (self.home / ".cache" / "poetry", "Python poetry cache"),
            (self.home / ".cache" / "pipenv", "Python pipenv cache"),
            (self.home / ".cache" / "uv", "Python uv cache"),
            # Node.js caches
            (self.home / ".npm", "Node.js npm cache"),
            (self.home / ".cache" / "yarn", "Node.js yarn cache"),
            (self.home / ".cache" / "fnm", "Node.js fnm cache"),
            # Go caches
            (self.home / ".cache" / "go-build", "Go build cache"),
            # Rust caches (if not removed by language managers cleanup)
            (self.home / ".cache" / "cargo", "Rust cargo cache"),
        ]
        
        for path, description in cache_dirs:
            self.remove_directory(path, description)
    
    def cleanup_system_caches(self) -> None:
        """Remove system and development tool caches"""
        print(f"\n🖥️  System Development Caches Cleanup")
        
        cache_dirs = [
            # Git caches
            (self.home / ".cache" / "git", "Git cache"),
            # Docker caches (if present)
            (self.home / ".docker" / "buildx", "Docker buildx cache"),
            # Xcode caches (macOS)
            (self.home / "Library" / "Developer" / "Xcode" / "DerivedData", "Xcode derived data"),
            (self.home / "Library" / "Caches" / "com.apple.dt.Xcode", "Xcode cache"),
            # General development caches
            (self.home / ".cache" / "bazel", "Bazel cache"),
            (self.home / ".gradle" / "caches", "Gradle cache"),
            (self.home / ".m2" / "repository", "Maven repository cache"),
        ]
        
        for path, description in cache_dirs:
            self.remove_directory(path, description)
    
    def cleanup_temporary_files(self) -> None:
        """Remove temporary files and directories"""
        print(f"\n🗑️  Temporary Files Cleanup")
        
        temp_dirs = [
            # Common temp directories
            (self.home / ".tmp", "User temp directory"),
            (Path("/tmp") / "homebrew-*", "Homebrew temp files (pattern)"),
        ]
        
        # Handle regular directories
        for path, description in temp_dirs:
            if "*" not in str(path):
                self.remove_directory(path, description)
        
        # Handle pattern-based cleanup for /tmp/homebrew-*
        try:
            tmp_dir = Path("/tmp")
            homebrew_temps = list(tmp_dir.glob("homebrew-*"))
            for temp_path in homebrew_temps:
                if temp_path.is_dir():
                    self.remove_directory(temp_path, f"Homebrew temp {temp_path.name}")
        except Exception as e:
            self.warning(f"Failed to clean homebrew temp files: {e}")
    
    def get_cleanup_summary(self) -> Dict[str, List[str]]:
        """Get summary of what will be cleaned"""
        return {
            "Homebrew": [
                "~/Library/Caches/Homebrew",
                "~/Library/Logs/Homebrew",
                "brew cleanup --prune=all"
            ],
            "Language Caches": [
                "~/.cache/pip, ~/.cache/poetry, ~/.cache/pipenv",
                "~/.npm, ~/.cache/yarn, ~/.cache/fnm",
                "~/.cache/go-build",
                "~/.cache/cargo (if present)"
            ],
            "System Caches": [
                "~/Library/Developer/Xcode/DerivedData",
                "~/Library/Caches/com.apple.dt.Xcode",
                "~/.gradle/caches, ~/.m2/repository",
                "~/.cache/bazel, ~/.cache/git"
            ],
            "Temporary Files": [
                "~/.tmp",
                "/tmp/homebrew-* (pattern)"
            ]
        }
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}🗑️  CACHES CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove various development caches:")
        print()
        
        summary = self.get_cleanup_summary()
        for category, items in summary.items():
            print(f"📂 {category}:")
            for item in items:
                print(f"  • {item}")
            print()
        
        print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]This may free up significant disk space but will require rebuilding caches")
        print()
    
    def run_cleanup(self, categories: List[str] = None) -> None:
        """Execute caches cleanup"""
        if categories is None:
            categories = ['all']
        
        self.show_summary()
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove development caches? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting caches cleanup...")
        
        # Execute cleanup based on categories
        if 'all' in categories:
            self.cleanup_homebrew_caches()
            self.cleanup_language_caches()
            self.cleanup_system_caches()
            self.cleanup_temporary_files()
        else:
            if 'homebrew' in categories:
                self.cleanup_homebrew_caches()
            if 'languages' in categories:
                self.cleanup_language_caches()
            if 'system' in categories:
                self.cleanup_system_caches()
            if 'temp' in categories:
                self.cleanup_temporary_files()
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Caches cleanup complete!{Colors.RESET}")
        print()
        print("Development caches have been removed.")
        print("Note: Some operations may be slower until caches are rebuilt.")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Caches Cleanup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Remove all caches (interactive)
  %(prog)s -y                 # Remove all caches (auto-confirm)
  %(prog)s -c homebrew        # Remove only Homebrew caches
  %(prog)s -c languages system # Remove language and system caches
        """
    )
    
    parser.add_argument('-y', '--yes', action='store_true',
                       help='Auto-confirm cleanup without asking')
    parser.add_argument('-c', '--categories', nargs='+',
                       choices=['homebrew', 'languages', 'system', 'temp', 'all'],
                       default=['all'],
                       help='Categories to clean (default: all)')
    
    args = parser.parse_args()
    
    cleanup = CachesCleanup(auto_confirm=args.yes)
    
    try:
        cleanup.run_cleanup(args.categories)
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()