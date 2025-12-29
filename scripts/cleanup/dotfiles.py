#!/usr/bin/env python3
"""
Dotfiles Cleanup Script
Removes dotfiles symlinks and configurations.
"""

import argparse
import shutil
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
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")
    
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
    
    def cleanup_zsh_dotfiles(self) -> None:
        """Remove zsh-related dotfiles"""
        print(f"\n🐚 Zsh Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".zshrc", "zsh configuration"),
            (self.home / ".zplug", "zplug directory"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_git_dotfiles(self) -> None:
        """Remove git-related dotfiles"""
        print(f"\n📝 Git Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".gitconfig", "git configuration"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_tmux_dotfiles(self) -> None:
        """Remove tmux-related dotfiles"""
        print(f"\n🖥️  Tmux Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".tmux.conf", "tmux configuration"),
            (self.home / ".tmux", "tmux directory"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_terminal_dotfiles(self) -> None:
        """Remove terminal-related dotfiles"""
        print(f"\n💻 Terminal Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".screenrc", "screen configuration"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_ssh_dotfiles(self) -> None:
        """Remove ssh-related dotfiles"""
        print(f"\n🔐 SSH Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".ssh" / "rc", "ssh configuration"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_tools_dotfiles(self) -> None:
        """Remove tools-related dotfiles"""
        print(f"\n🛠️  Tools Configuration Cleanup")
        
        dotfiles = [
            (self.home / ".tools", "tools directory"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def cleanup_neovim_symlinks(self) -> None:
        """Remove neovim configuration symlinks (not dynamic content)"""
        print(f"\n📝 Neovim Configuration Symlinks Cleanup")
        
        dotfiles = [
            (self.home / ".config" / "nvim", "neovim config directory symlink"),
        ]
        
        for path, description in dotfiles:
            self.remove_file_or_symlink(path, description)
    
    def get_cleanup_summary(self) -> Dict[str, List[str]]:
        """Get summary of what will be cleaned"""
        return {
            "Zsh": [
                "~/.zshrc (zsh configuration)",
                "~/.zplug (zplug directory)"
            ],
            "Git": [
                "~/.gitconfig (git configuration)"
            ],
            "Tmux": [
                "~/.tmux.conf (tmux configuration)",
                "~/.tmux (tmux directory)"
            ],
            "Terminal": [
                "~/.screenrc (screen configuration)"
            ],
            "SSH": [
                "~/.ssh/rc (ssh configuration)"
            ],
            "Tools": [
                "~/.tools (tools directory)"
            ],
            "Neovim": [
                "~/.config/nvim (config symlink only)"
            ]
        }
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}⚙️  DOTFILES CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove all dotfiles symlinks:")
        print()
        
        summary = self.get_cleanup_summary()
        for category, items in summary.items():
            print(f"📂 {category}:")
            for item in items:
                print(f"  • {item}")
            print()
        
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Original config files in the repository will be preserved")
        print()
    
    def run_cleanup(self, categories: List[str] = None) -> None:
        """Execute dotfiles cleanup"""
        if categories is None:
            categories = ['all']
        
        self.show_summary()
        
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
        
        # Execute cleanup based on categories
        if 'all' in categories:
            self.cleanup_zsh_dotfiles()
            self.cleanup_git_dotfiles()
            self.cleanup_tmux_dotfiles()
            self.cleanup_terminal_dotfiles()
            self.cleanup_ssh_dotfiles()
            self.cleanup_tools_dotfiles()
            self.cleanup_neovim_symlinks()
        else:
            if 'zsh' in categories:
                self.cleanup_zsh_dotfiles()
            if 'git' in categories:
                self.cleanup_git_dotfiles()
            if 'tmux' in categories:
                self.cleanup_tmux_dotfiles()
            if 'terminal' in categories:
                self.cleanup_terminal_dotfiles()
            if 'ssh' in categories:
                self.cleanup_ssh_dotfiles()
            if 'tools' in categories:
                self.cleanup_tools_dotfiles()
            if 'neovim' in categories:
                self.cleanup_neovim_symlinks()
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Dotfiles cleanup complete!{Colors.RESET}")
        print()
        print("All dotfiles symlinks have been removed.")
        print("You can recreate them with: make dotfiles")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Dotfiles Cleanup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Remove all dotfiles (interactive)
  %(prog)s -y                 # Remove all dotfiles (auto-confirm)
  %(prog)s -c zsh git         # Remove only zsh and git dotfiles
  %(prog)s -c neovim          # Remove only neovim symlinks
        """
    )
    
    parser.add_argument('-y', '--yes', action='store_true',
                       help='Auto-confirm cleanup without asking')
    parser.add_argument('-c', '--categories', nargs='+',
                       choices=['zsh', 'git', 'tmux', 'terminal', 'ssh', 'tools', 'neovim', 'all'],
                       default=['all'],
                       help='Categories to clean (default: all)')
    
    args = parser.parse_args()
    
    cleanup = DotfilesCleanup(auto_confirm=args.yes)
    
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