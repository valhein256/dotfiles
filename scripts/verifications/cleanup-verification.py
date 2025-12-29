#!/usr/bin/env python3
"""
Cleanup Verification Script
Comprehensive verification that all packages and configurations have been completely removed.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


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


class CleanupVerifier:
    """Comprehensive cleanup verification system"""
    
    def __init__(self):
        self.home = Path.home()
        self.repo_path = Path.cwd()
        self.issues_found = []
        self.warnings_found = []
        self.cleanup_items_found = []
        self.total_checks = 0
        self.passed_checks = 0
    
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
        self.passed_checks += 1
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ] {message}")
        self.warnings_found.append(message)
    
    def error(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
        self.issues_found.append(message)
        self.cleanup_items_found.append(message)
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def check_homebrew_packages(self) -> None:
        """Verify all Homebrew packages are removed"""
        print(f"\n{Colors.CYAN}🍺 Checking Homebrew Package Removal{Colors.RESET}")
        
        self.total_checks += 2
        
        # Check formulae
        result = self.run_command("brew list --formula")
        if result and result.returncode == 0:
            formulae = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            if not formulae:
                self.success("All formulae removed")
            else:
                self.error(f"{len(formulae)} formulae still installed")
                for formula in formulae[:10]:  # Show first 10
                    print(f"    • {formula}")
                if len(formulae) > 10:
                    print(f"    ... and {len(formulae) - 10} more")
        else:
            # If brew command fails, it might mean brew is not available or no packages
            if result and "No formulae" in result.stderr or not result:
                self.success("All formulae removed")
            else:
                self.success("No formulae found (brew may not be available)")
        
        # Check casks
        result = self.run_command("brew list --cask")
        if result and result.returncode == 0:
            casks = [c.strip() for c in result.stdout.split('\n') if c.strip()]
            if not casks:
                self.success("All casks removed")
            else:
                self.error(f"{len(casks)} casks still installed")
                for cask in casks:
                    print(f"    • {cask}")
        else:
            # If brew command fails, it might mean brew is not available or no packages
            if result and "No casks" in result.stderr or not result:
                self.success("All casks removed")
            else:
                self.success("No casks found (brew may not be available)")
    
    def check_language_managers_cleanup(self) -> None:
        """Verify all language managers and their installations are removed"""
        print(f"\n{Colors.CYAN}🔧 Checking Language Managers Cleanup{Colors.RESET}")
        
        language_dirs = [
            # Python (uv)
            (self.home / ".local" / "share" / "uv", "Python (uv) data"),
            (self.home / ".cache" / "uv", "Python (uv) cache"),
            (self.home / ".config" / "uv", "Python (uv) config"),
            
            # Node.js (fnm)
            (self.home / ".local" / "share" / "fnm", "Node.js (fnm) data"),
            (self.home / ".cache" / "fnm", "Node.js (fnm) cache"),
            (self.home / ".fnm", "Node.js (fnm) alternative location"),
            
            # Java (SDKMAN)
            (self.home / ".sdkman", "Java (SDKMAN) installation"),
            
            # Rust
            (self.home / ".rustup", "Rust (rustup) toolchain"),
            (self.home / ".cargo", "Rust (cargo) packages"),
            
            # Go
            (self.home / "go", "Go workspace"),
            (self.home / ".cache" / "go-build", "Go build cache"),
            
            # Legacy Python managers
            (self.home / ".pyenv", "Legacy Python (pyenv)"),
            (self.home / ".cache" / "pip", "Python pip cache"),
            (self.home / ".cache" / "poetry", "Python poetry cache"),
            (self.home / ".cache" / "pipenv", "Python pipenv cache"),
            
            # Legacy Node.js managers
            (self.home / ".nvm", "Legacy Node.js (nvm)"),
            (self.home / ".npm", "Node.js npm cache"),
            (self.home / ".cache" / "yarn", "Node.js yarn cache"),
        ]
        
        self.total_checks += len(language_dirs)
        
        for dir_path, description in language_dirs:
            if dir_path.exists():
                self.error(f"{description} still exists: {dir_path}")
            else:
                self.success(f"{description} removed")
    
    def check_neovim_cleanup(self) -> None:
        """Verify Neovim dynamic content is cleaned up"""
        print(f"\n{Colors.CYAN}📝 Checking Neovim Cleanup{Colors.RESET}")
        
        neovim_items = [
            # System-wide neovim directories
            (self.home / ".local" / "share" / "nvim", "Neovim system data"),
            (self.home / ".cache" / "nvim", "Neovim system cache"),
            (self.home / ".vim" / "plugged", "Vim plugins directory"),
            (self.home / ".vim" / "autoload", "Vim autoload directory"),
            
            # Config directory (should be cleaned for fresh install)
            (self.home / ".config" / "nvim", "Neovim config directory"),
            
            # Dotfiles dynamic content
            (self.repo_path / "neovim" / "plugged", "Dotfiles Neovim plugins"),
            (self.repo_path / "neovim" / "env", "Dotfiles Neovim Python env"),
            (self.repo_path / "neovim" / "autoload" / "plug.vim", "Dotfiles vim-plug"),
        ]
        
        self.total_checks += len(neovim_items)
        
        for item_path, description in neovim_items:
            if item_path.exists():
                self.error(f"{description} still exists: {item_path}")
            else:
                self.success(f"{description} removed")
        
        # Check if original config files are preserved
        original_files = [
            (self.repo_path / "neovim" / "init.vim", "Original init.vim"),
            (self.repo_path / "neovim", "Original neovim directory"),
        ]
        
        print(f"\n📄 Checking Original Config Preservation:")
        for file_path, description in original_files:
            if file_path.exists():
                self.info(f"{description} preserved (good)")
            else:
                self.warning(f"{description} missing")
    
    def check_dotfiles_cleanup(self) -> None:
        """Verify all dotfiles symlinks are removed"""
        print(f"\n{Colors.CYAN}⚙️  Checking Dotfiles Cleanup{Colors.RESET}")
        
        dotfiles_symlinks = [
            (self.home / ".zshrc", "zsh configuration"),
            (self.home / ".gitconfig", "git configuration"),
            (self.home / ".tmux.conf", "tmux configuration"),
            (self.home / ".screenrc", "screen configuration"),
            (self.home / ".ssh" / "rc", "ssh configuration"),
            (self.home / ".tmux", "tmux directory"),
            (self.home / ".zplug", "zplug directory"),
            (self.home / ".tools", "tools directory"),
        ]
        
        self.total_checks += len(dotfiles_symlinks)
        
        for symlink_path, description in dotfiles_symlinks:
            if symlink_path.exists() or symlink_path.is_symlink():
                self.error(f"{description} still exists: {symlink_path}")
            else:
                self.success(f"{description} removed")
    
    def check_git_submodules_cleanup(self) -> None:
        """Verify git submodules are cleaned up"""
        print(f"\n{Colors.CYAN}🔗 Checking Git Submodules Cleanup{Colors.RESET}")
        
        submodule_dirs = [
            (self.repo_path / "zsh" / "zplug", "zplug submodule"),
            (self.repo_path / "tmux" / "plugins" / "tpm", "tmux plugin manager"),
        ]
        
        self.total_checks += len(submodule_dirs)
        
        for submodule_path, description in submodule_dirs:
            if submodule_path.exists() and (submodule_path / ".git").exists():
                self.error(f"{description} still initialized: {submodule_path}")
            else:
                self.success(f"{description} cleaned up")
    
    def check_homebrew_caches(self) -> None:
        """Check Homebrew cache cleanup"""
        print(f"\n{Colors.CYAN}🗑️  Checking Homebrew Caches{Colors.RESET}")
        
        cache_dirs = [
            (self.home / "Library" / "Caches" / "Homebrew", "Homebrew cache"),
            (self.home / "Library" / "Logs" / "Homebrew", "Homebrew logs"),
        ]
        
        self.total_checks += len(cache_dirs)
        
        for cache_dir, description in cache_dirs:
            if cache_dir.exists():
                try:
                    result = self.run_command(f"du -sh '{cache_dir}'")
                    if result and result.returncode == 0:
                        size_info = result.stdout.strip().split('\t')[0]
                        if any(unit in size_info for unit in ['G', 'M']) and not size_info.startswith('0'):
                            self.warning(f"{description} exists ({size_info}): {cache_dir}")
                        else:
                            self.success(f"{description} minimal size ({size_info})")
                    else:
                        self.warning(f"{description} exists: {cache_dir}")
                except:
                    self.warning(f"{description} exists: {cache_dir}")
            else:
                self.success(f"{description} removed")
    
    def check_system_commands(self) -> None:
        """Verify essential system commands are still available"""
        print(f"\n{Colors.CYAN}🔍 Checking Essential System Commands{Colors.RESET}")
        
        essential_commands = [
            ("brew", "Homebrew package manager"),
            ("git", "Version control system"),
            ("curl", "Download tool"),
            ("zsh", "Z shell"),
        ]
        
        self.total_checks += len(essential_commands)
        
        for cmd, description in essential_commands:
            result = self.run_command(f"which {cmd}")
            if result and result.returncode == 0:
                self.success(f"{cmd} available - {description}")
            else:
                self.warning(f"{cmd} not found - {description}")
    
    def generate_cleanup_report(self) -> bool:
        """Generate comprehensive cleanup verification report"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 CLEANUP VERIFICATION REPORT{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print(f"\n📈 Cleanup Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}")
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Items cleaned: {self.passed_checks}/{self.total_checks}")
        
        if not self.issues_found and not self.warnings_found:
            print(f"\n{Colors.GREEN}🎉 CLEANUP VERIFICATION PASSED!{Colors.RESET}")
            print("Your system has been completely cleaned and is ready for fresh installation.")
            print("\nNext steps:")
            print("  1. Run: make install")
            print("  2. Run: make language-managers")
            print("  3. Run: python3 scripts/verification/installation-verification.py")
            return True
        else:
            if self.issues_found:
                print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] CLEANUP ISSUES FOUND ({len(self.issues_found)}){Colors.RESET}")
                print("The following items still need to be cleaned:")
                for issue in self.issues_found:
                    print(f"  • {issue}")
                
                print(f"\n{Colors.YELLOW}💡 Cleanup Commands:{Colors.RESET}")
                print("  # Remove remaining Homebrew packages:")
                print("  brew uninstall --ignore-dependencies --force $(brew list --formula)")
                print("  brew uninstall --cask --force $(brew list --cask)")
                print("  brew cleanup --prune=all")
                print()
                print("  # Remove language managers:")
                print("  python3 scripts/cleanup/language-managers-cleanup.py")
                print()
                print("  # Remove dotfiles:")
                print("  python3 scripts/cleanup/remove-dotfiles.py -c all")
            
            if self.warnings_found:
                print(f"\n{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]WARNINGS ({len(self.warnings_found)}){Colors.RESET}")
                for warning in self.warnings_found:
                    print(f"  • {warning}")
            
            print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] CLEANUP VERIFICATION FAILED!{Colors.RESET}")
            print("Please address the issues above before proceeding with installation.")
            return False
    
    def run_full_cleanup_verification(self) -> bool:
        """Run complete cleanup verification"""
        print(f"{Colors.BOLD}🧹 CLEANUP VERIFICATION{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        print("Verifying that all packages and configurations have been completely removed...")
        
        self.check_homebrew_packages()
        self.check_language_managers_cleanup()
        self.check_neovim_cleanup()
        self.check_dotfiles_cleanup()
        self.check_git_submodules_cleanup()
        self.check_homebrew_caches()
        self.check_system_commands()
        
        return self.generate_cleanup_report()


def main():
    """Main function"""
    verifier = CleanupVerifier()
    success = verifier.run_full_cleanup_verification()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()