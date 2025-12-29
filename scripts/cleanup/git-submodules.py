#!/usr/bin/env python3
"""
Git Submodules Cleanup Script
Removes and deinitializes git submodules.
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


class GitSubmodulesCleanup:
    """Git submodules cleanup manager"""
    
    def __init__(self, auto_confirm: bool = False):
        self.auto_confirm = auto_confirm
        self.repo_path = Path.cwd()
        
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def fail(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
    
    def run_command(self, cmd: str, capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True, cwd=self.repo_path)
            return result
        except Exception as e:
            self.warning(f"Command failed: {cmd} - {e}")
            return None
    
    def remove_directory(self, path: Path, description: str) -> None:
        """Safely remove a directory and all its contents"""
        if path.exists():
            self.info(f"Removing {description} at {path}")
            try:
                shutil.rmtree(path)
                self.success(f"{description} removed")
            except Exception as e:
                self.warning(f"Failed to remove {description}: {e}")
        else:
            self.success(f"{description} not found (already clean)")
    
    def get_submodule_paths(self) -> List[str]:
        """Get list of submodule paths from .gitmodules"""
        gitmodules_path = self.repo_path / ".gitmodules"
        submodule_paths = []
        
        if not gitmodules_path.exists():
            return submodule_paths
        
        try:
            with open(gitmodules_path, 'r') as f:
                content = f.read()
            
            # Parse .gitmodules file
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('path = '):
                    path = line.replace('path = ', '').strip()
                    submodule_paths.append(path)
                    
        except Exception as e:
            self.warning(f"Failed to parse .gitmodules: {e}")
        
        return submodule_paths
    
    def deinitialize_submodules(self) -> None:
        """Deinitialize all git submodules"""
        print(f"\n🔗 Git Submodules Deinitialization")
        
        self.info("Deinitializing all git submodules...")
        result = self.run_command("git submodule deinit --all --force", capture_output=False)
        
        if result and result.returncode == 0:
            self.success("Git submodules deinitialized")
        else:
            self.warning("Git submodule deinit command may have failed")
    
    def remove_submodule_directories(self) -> None:
        """Remove submodule directories"""
        print(f"\n📁 Submodule Directories Cleanup")
        
        # Known submodule paths
        known_submodules = [
            ("zsh/zplug", "zplug submodule"),
            ("tmux/plugins/tpm", "tmux plugin manager"),
        ]
        
        # Also get paths from .gitmodules
        gitmodules_paths = self.get_submodule_paths()
        for path in gitmodules_paths:
            if path not in [sm[0] for sm in known_submodules]:
                known_submodules.append((path, f"submodule {path}"))
        
        # Remove each submodule directory
        for submodule_path, description in known_submodules:
            full_path = self.repo_path / submodule_path
            self.remove_directory(full_path, description)
    
    def clean_git_submodule_cache(self) -> None:
        """Clean git submodule cache"""
        print(f"\n🗑️  Git Submodule Cache Cleanup")
        
        # Remove .git/modules directory (submodule git data)
        git_modules = self.repo_path / ".git" / "modules"
        if git_modules.exists():
            self.remove_directory(git_modules, "git submodules cache")
        else:
            self.success("Git submodules cache not found (already clean)")
    
    def get_cleanup_summary(self) -> Dict[str, List[str]]:
        """Get summary of what will be cleaned"""
        submodule_paths = self.get_submodule_paths()
        
        return {
            "Submodule Directories": [
                "zsh/zplug (zsh plugin manager)",
                "tmux/plugins/tpm (tmux plugin manager)",
            ] + [f"{path} (from .gitmodules)" for path in submodule_paths if path not in ["zsh/zplug", "tmux/plugins/tpm"]],
            "Git Data": [
                ".git/modules (submodule git cache)"
            ],
            "Operations": [
                "git submodule deinit --all --force"
            ]
        }
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}🔗 GIT SUBMODULES CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will clean up all git submodules:")
        print()
        
        summary = self.get_cleanup_summary()
        for category, items in summary.items():
            print(f"📂 {category}:")
            for item in items:
                print(f"  • {item}")
            print()
        
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Main repository and .gitmodules file will be preserved")
        print()
    
    def run_cleanup(self) -> None:
        """Execute git submodules cleanup"""
        self.show_summary()
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Clean up git submodules? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting git submodules cleanup...")
        
        # Execute cleanup
        self.deinitialize_submodules()
        self.remove_submodule_directories()
        self.clean_git_submodule_cache()
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Git submodules cleanup complete!{Colors.RESET}")
        print()
        print("All git submodules have been deinitialized and removed.")
        print("You can reinitialize them with: make git-submodule")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Git Submodules Cleanup Script",
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
    
    cleanup = GitSubmodulesCleanup(auto_confirm=args.yes)
    
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