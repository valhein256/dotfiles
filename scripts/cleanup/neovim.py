#!/usr/bin/env python3
"""
Neovim Cleanup Script
Removes Neovim dynamic content while preserving configuration files.
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


class NeovimCleanup:
    """Neovim cleanup manager"""
    
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
    
    def remove_file(self, path: Path, description: str) -> None:
        """Safely remove a file or symlink"""
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
    
    def cleanup_system_neovim_data(self) -> None:
        """Remove system-wide Neovim data directories"""
        print(f"\n🖥️  System Neovim Data Cleanup")
        
        directories = [
            (self.home / ".local" / "share" / "nvim", "Neovim system data"),
            (self.home / ".cache" / "nvim", "Neovim system cache"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_vim_legacy_data(self) -> None:
        """Remove legacy Vim data directories"""
        print(f"\n📝 Legacy Vim Data Cleanup")
        
        directories = [
            (self.home / ".vim" / "plugged", "Vim plugins directory"),
            (self.home / ".vim" / "autoload", "Vim autoload directory"),
        ]
        
        for path, description in directories:
            self.remove_directory(path, description)
    
    def cleanup_neovim_config_symlink(self) -> None:
        """Remove Neovim config directory symlink"""
        print(f"\n🔗 Neovim Config Symlink Cleanup")
        
        config_path = self.home / ".config" / "nvim"
        self.remove_file(config_path, "Neovim config directory symlink")
    
    def cleanup_dotfiles_neovim_dynamic(self) -> None:
        """Remove dynamic content from dotfiles neovim directory"""
        print(f"\n📁 Dotfiles Neovim Dynamic Content Cleanup")
        
        dynamic_content = [
            (self.repo_path / "neovim" / "plugged", "Neovim plugins directory"),
            (self.repo_path / "neovim" / "env", "Neovim Python environment"),
            (self.repo_path / "neovim" / "autoload" / "plug.vim", "vim-plug file"),
        ]
        
        for path, description in dynamic_content:
            if path.is_dir():
                self.remove_directory(path, description)
            else:
                self.remove_file(path, description)
    
    def check_preserved_files(self) -> None:
        """Check and report on preserved configuration files"""
        print(f"\n[ {Colors.GREEN}OK{Colors.RESET} ] Preserved Configuration Files")
        
        preserved_files = [
            self.repo_path / "neovim" / "init.vim",
            self.repo_path / "neovim" / "vimfiles",
            self.repo_path / "neovim",  # Directory itself
        ]
        
        for file_path in preserved_files:
            if file_path.exists():
                self.info(f"Preserved: {file_path}")
            else:
                self.warning(f"Original file not found: {file_path}")
    
    def get_cleanup_summary(self) -> Dict[str, List[str]]:
        """Get summary of what will be cleaned"""
        return {
            "System Data": [
                "~/.local/share/nvim (Neovim data)",
                "~/.cache/nvim (Neovim cache)"
            ],
            "Legacy Vim": [
                "~/.vim/plugged (Vim plugins)",
                "~/.vim/autoload (Vim autoload)"
            ],
            "Config Symlink": [
                "~/.config/nvim (symlink only)"
            ],
            "Dynamic Content": [
                "./neovim/plugged (plugins)",
                "./neovim/env (Python environment)",
                "./neovim/autoload/plug.vim (vim-plug)"
            ],
            "Preserved": [
                "./neovim/init.vim (original config)",
                "./neovim/vimfiles (original files)",
                "./neovim/ (directory structure)"
            ]
        }
    
    def show_summary(self) -> None:
        """Show what will be cleaned up"""
        print(f"\n{Colors.CYAN}📝 NEOVIM CLEANUP{Colors.RESET}")
        print("=" * 50)
        print()
        print("This will remove Neovim dynamic content:")
        print()
        
        summary = self.get_cleanup_summary()
        for category, items in summary.items():
            if category == "Preserved":
                print(f"[ {Colors.GREEN}OK{Colors.RESET} ] {category}:")
            else:
                print(f"🗑️  {category}:")
            for item in items:
                print(f"  • {item}")
            print()
        
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Original configuration files will be preserved{Colors.RESET}")
        print()
    
    def run_cleanup(self) -> None:
        """Execute Neovim cleanup"""
        self.show_summary()
        
        # Get confirmation
        if self.auto_confirm:
            print("🤖 Auto-confirmation enabled, proceeding with cleanup...")
        else:
            confirmation = input("❓ Remove Neovim dynamic content? Type 'YES' to confirm: ")
            if confirmation != "YES":
                print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Operation cancelled")
                return
        
        print()
        self.info("Starting Neovim cleanup...")
        
        # Execute cleanup
        self.cleanup_system_neovim_data()
        self.cleanup_vim_legacy_data()
        self.cleanup_neovim_config_symlink()
        self.cleanup_dotfiles_neovim_dynamic()
        self.check_preserved_files()
        
        print()
        print(f"{Colors.GREEN}[ {Colors.GREEN}OK{Colors.RESET} ] Neovim cleanup complete!{Colors.RESET}")
        print()
        print("All Neovim dynamic content has been removed.")
        print("Original configuration files have been preserved.")
        print("You can reinstall plugins with: make neovim-plugins")
        print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Neovim Cleanup Script",
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
    
    cleanup = NeovimCleanup(auto_confirm=args.yes)
    
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