#!/usr/bin/env python3
"""
Git Submodule Management Script
Initializes and updates git submodules for zsh and tmux plugins.
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
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    GRAY = '\033[90m'


class GitSubmoduleManager:
    """Git submodule management system"""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.platform = os.uname().sysname
        
        # Define submodules
        self.submodules = [
            ("https://github.com/zplug/zplug", "zsh/zplug", "zplug"),
            ("https://github.com/tmux-plugins/tpm", "tmux/plugins/tpm", "tmux plugin manager"),
        ]
    
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
    
    def fail(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
        print("")
        sys.exit(1)
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
    def run_command(self, cmd: List[str], description: str = "", capture_output: bool = False) -> subprocess.CompletedProcess:
        """Run a command and handle errors"""
        try:
            if not capture_output:
                self.info(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=self.current_path,
                capture_output=capture_output,
                text=True,
                check=True
            )
            
            if description and not capture_output:
                self.success(description)
            
            return result
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {' '.join(cmd)}"
            if e.stderr:
                error_msg += f"\nError: {e.stderr}"
            self.fail(error_msg)
        except Exception as e:
            self.fail(f"Unexpected error running command: {e}")
    
    def check_git_repository(self) -> bool:
        """Check if we're in a git repository"""
        try:
            self.run_command(["git", "rev-parse", "--git-dir"], capture_output=True)
            return True
        except:
            return False
    
    def has_gitmodules(self) -> bool:
        """Check if .gitmodules file exists"""
        return (self.current_path / ".gitmodules").exists()
    
    def add_submodules(self) -> None:
        """Add submodules if .gitmodules doesn't exist"""
        if self.has_gitmodules():
            self.info(".gitmodules already exists, skipping submodule addition")
            return
        
        self.info("Adding git submodules...")
        
        for url, path, description in self.submodules:
            self.info(f"Adding {description} submodule...")
            try:
                self.run_command([
                    "git", "submodule", "add", url, path
                ], f"{description} submodule added")
            except:
                # If submodule already exists, continue
                self.warning(f"{description} submodule may already exist")
    
    def init_submodules(self) -> None:
        """Initialize git submodules"""
        self.info("Initializing git submodules...")
        self.run_command([
            "git", "submodule", "init"
        ], "Git submodules initialized")
    
    def update_submodules(self) -> None:
        """Update git submodules recursively"""
        self.info("Updating git submodules...")
        self.run_command([
            "git", "submodule", "update", "--recursive"
        ], "Git submodules updated")
    
    def pull_submodules(self) -> None:
        """Pull latest changes for all submodules"""
        self.info("Pulling latest changes for submodules...")
        self.run_command([
            "git", "submodule", "foreach", "--recursive", "git", "pull", "origin", "master"
        ], "Submodules pulled to latest")
    
    def verify_submodules(self) -> bool:
        """Verify that all submodules are properly initialized"""
        self.info("Verifying submodules...")
        
        all_good = True
        for _, path, description in self.submodules:
            submodule_path = self.current_path / path
            git_path = submodule_path / ".git"
            
            if submodule_path.exists() and git_path.exists():
                self.success(f"{description} submodule verified")
            else:
                self.warning(f"{description} submodule not properly initialized")
                all_good = False
        
        return all_good
    
    def setup_submodules(self) -> None:
        """Complete submodule setup process"""
        print("")
        print(f"{Colors.GRAY}##########################################")
        print(f"# scripts/installations/git-submodule.py #")
        print(f"##########################################{Colors.RESET}")
        print("")
        print("### Git submodule init & update...")
        
        # Check if we're in a git repository
        if not self.check_git_repository():
            self.fail("Not in a git repository")
        
        # Add submodules if needed
        self.add_submodules()
        
        # Initialize submodules
        self.init_submodules()
        
        # Update submodules
        self.update_submodules()
        
        # Pull latest changes
        self.pull_submodules()
        
        print("### Git submodule init & update... done !!")
        print("")
        print(f"{Colors.GREEN}# scripts/installations/git-submodule.py Finish !!{Colors.RESET}")
        print("")
    
    def status(self) -> None:
        """Show submodule status"""
        print("📋 Git Submodule Status:")
        try:
            result = self.run_command([
                "git", "submodule", "status"
            ], capture_output=True)
            
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    print(f"  {line}")
            else:
                print("  No submodules found")
                
        except:
            print("  Failed to get submodule status")


def main():
    """Main function"""
    manager = GitSubmoduleManager()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            manager.status()
            return
        elif sys.argv[1] == "--verify":
            success = manager.verify_submodules()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--help":
            print("Git Submodule Manager")
            print("Usage:")
            print("  python git-submodule.py          # Setup submodules")
            print("  python git-submodule.py --status # Show status")
            print("  python git-submodule.py --verify # Verify setup")
            return
    
    try:
        manager.setup_submodules()
        
        # Verify installation
        if manager.verify_submodules():
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] All submodules successfully set up!")
        else:
            print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]Some submodules may need attention")
            
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()