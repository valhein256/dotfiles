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
        """Install all dotfiles by creating symbolic links"""
        print("")
        print(f"{Colors.GRAY}#####################################")
        print(f"# scripts/installations/dotfiles.py #")
        print(f"#####################################{Colors.RESET}")
        print("")
        print("### Dotfiles setting...")
        
        # Define dotfiles to be linked
        dotfiles = [
            (self.current_path / "gitconfig", self.home / ".gitconfig", "gitconfig"),
            (self.current_path / "screenrc", self.home / ".screenrc", "screenrc"),
            (self.current_path / "sshrc", self.home / ".ssh" / "rc", "sshrc"),
            (self.current_path / "zsh" / "zshrc", self.home / ".zshrc", "zshrc"),
        ]
        
        # Define directories to be linked
        directories = [
            (self.current_path / "zsh" / "zplug", self.home / ".zplug", "zplug"),
            (self.current_path / "tmux", self.home / ".tmux", "tmux"),
            (self.current_path / "tools", self.home / ".tools", "tools"),
        ]
        
        # Install individual dotfiles
        for source, target, description in dotfiles:
            if not source.exists():
                self.warning(f"Source file not found: {source}")
                continue
            
            self.info(f"{description} setting...")
            self.create_symlink(source, target, description)
        
        # Install directory links
        for source, target, description in directories:
            if not source.exists():
                self.warning(f"Source directory not found: {source}")
                continue
            
            self.info(f"{description} setting...")
            self.create_symlink(source, target, description)
        
        # Special handling for tmux.conf (link to the file inside the tmux directory)
        tmux_conf_source = self.home / ".tmux" / "tmux.conf"
        tmux_conf_target = self.home / ".tmux.conf"
        
        if tmux_conf_source.exists():
            self.info("tmux.conf setting...")
            self.create_symlink(tmux_conf_source, tmux_conf_target, "tmux.conf")
        
        print("### Dotfiles setting... done !!")
        print("")
        print(f"{Colors.GREEN}# scripts/installations/dotfiles.py Finish !!{Colors.RESET}")
        print("")
    
    def verify_installation(self) -> bool:
        """Verify that all symlinks are correctly created"""
        print("🔍 Verifying dotfiles installation...")
        
        expected_links = [
            (self.home / ".gitconfig", "gitconfig"),
            (self.home / ".screenrc", "screenrc"),
            (self.home / ".ssh" / "rc", "sshrc"),
            (self.home / ".zshrc", "zshrc"),
            (self.home / ".zplug", "zplug"),
            (self.home / ".tmux", "tmux"),
            (self.home / ".tmux.conf", "tmux.conf"),
            (self.home / ".tools", "tools"),
        ]
        
        all_good = True
        for target, description in expected_links:
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