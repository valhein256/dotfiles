#!/usr/bin/env python3
"""
Post-Installation Verification Script
Comprehensive verification of the development environment after installation.
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


class PostInstallVerifier:
    """Post-installation verification system"""
    
    def __init__(self):
        self.home = Path.home()
        self.repo_path = Path.cwd()
        self.issues_found = []
        self.warnings_found = []
        self.success_count = 0
        self.total_checks = 0
    
    def info(self, message: str) -> None:
        print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")
    
    def success(self, message: str) -> None:
        print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")
        self.success_count += 1
    
    def warning(self, message: str) -> None:
        print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ] {message}")
        self.warnings_found.append(message)
    
    def error(self, message: str) -> None:
        print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
        self.issues_found.append(message)
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def verify_essential_packages(self) -> None:
        """Verify all essential packages are installed"""
        print(f"\n{Colors.CYAN}📦 Verifying Essential Packages{Colors.RESET}")
        
        essential_packages = [
            "zsh", "git", "tree", "fzf", "ripgrep",  # core
            "neovim", "universal-ctags",  # editor
            "tmux",  # terminal
            "uv",  # python
            "fnm", "pnpm",  # nodejs
            "go",  # golang
            "zip", "unzip", "curl",  # java-prereq
            "kubectl", "helm", "terraform", "terragrunt",  # devops
            "awscli",  # cloud
            "openssh", "sshs", "teleport",  # network
        ]
        
        self.total_checks += len(essential_packages)
        
        for package in essential_packages:
            result = self.run_command(f"brew list {package}")
            if result and result.returncode == 0:
                self.success(f"{package}")
            else:
                self.error(f"{package} not installed")
    
    def verify_language_environments(self) -> None:
        """Verify language environments are properly set up"""
        print(f"\n{Colors.CYAN}🔧 Verifying Language Environments{Colors.RESET}")
        
        # Python (uv)
        self.total_checks += 1
        result = self.run_command("uv python list")
        if result and result.returncode == 0 and result.stdout.strip():
            self.success("Python (uv) - versions installed")
        else:
            self.error("Python (uv) - no versions found")
        
        # Node.js (fnm)
        self.total_checks += 1
        result = self.run_command("fnm list")
        if result and result.returncode == 0 and "No Node.js versions" not in result.stdout:
            self.success("Node.js (fnm) - versions installed")
        else:
            self.error("Node.js (fnm) - no versions found")
        
        # Java (SDKMAN)
        self.total_checks += 1
        sdkman_dir = self.home / ".sdkman"
        if sdkman_dir.exists():
            java_dir = sdkman_dir / "candidates" / "java"
            if java_dir.exists() and any(java_dir.iterdir()):
                self.success("Java (SDKMAN) - versions installed")
            else:
                self.error("Java (SDKMAN) - no versions found")
        else:
            self.error("Java (SDKMAN) - not installed")
        
        # Rust
        self.total_checks += 1
        result = self.run_command("rustc --version")
        if result and result.returncode == 0:
            self.success("Rust - toolchain available")
        else:
            self.error("Rust - toolchain not available")
        
        # Go
        self.total_checks += 1
        result = self.run_command("go version")
        if result and result.returncode == 0:
            self.success("Go - available")
        else:
            self.error("Go - not available")
    
    def verify_dotfiles_configuration(self) -> None:
        """Verify dotfiles are properly configured"""
        print(f"\n{Colors.CYAN}⚙️  Verifying Dotfiles Configuration{Colors.RESET}")
        
        # Define expected symlinks
        expected_symlinks = [
            (self.home / ".zshrc", "zsh/zshrc"),
            (self.home / ".gitconfig", "gitconfig"),
            (self.home / ".tmux.conf", "tmux/tmux.conf"),
            (self.home / ".screenrc", "screenrc"),
            (self.home / ".ssh" / "rc", "sshrc"),
            (self.home / ".tmux", "tmux"),
            (self.home / ".zplug", "zsh/zplug"),
            (self.home / ".tools", "tools"),
        ]
        
        for home_path, repo_path in expected_symlinks:
            self.total_checks += 1
            if home_path.exists() and home_path.is_symlink():
                target = home_path.resolve()
                expected_target = self.repo_path / repo_path
                if target == expected_target:
                    self.success(f"{home_path.name} correctly symlinked")
                else:
                    self.error(f"{home_path.name} symlinked to wrong target")
            else:
                self.error(f"{home_path.name} not properly symlinked")
    
    def verify_neovim_setup(self) -> None:
        """Verify Neovim is properly set up"""
        print(f"\n{Colors.CYAN}📝 Verifying Neovim Setup{Colors.RESET}")
        
        # Check Neovim symlink
        self.total_checks += 1
        nvim_config = self.home / ".config" / "nvim"
        if nvim_config.exists() and nvim_config.is_symlink():
            target = nvim_config.resolve()
            expected_target = self.repo_path / "neovim"
            if target == expected_target:
                self.success("Neovim config correctly symlinked")
            else:
                self.error("Neovim config symlinked to wrong target")
        else:
            self.error("Neovim config not properly symlinked")
        
        # Check Python environment
        self.total_checks += 1
        python_env = self.repo_path / "neovim" / "env"
        if python_env.exists() and (python_env / "bin" / "python").exists():
            self.success("Neovim Python environment created")
        else:
            self.error("Neovim Python environment missing")
        
        # Check vim-plug
        self.total_checks += 1
        plug_vim = self.repo_path / "neovim" / "autoload" / "plug.vim"
        if plug_vim.exists():
            self.success("vim-plug installed")
        else:
            self.error("vim-plug not installed")
        
        # Check if plugins directory exists (may be empty initially)
        self.total_checks += 1
        plugged_dir = self.repo_path / "neovim" / "plugged"
        if plugged_dir.exists():
            self.success("Neovim plugins directory created")
        else:
            self.warning("Neovim plugins directory not found")
    
    def verify_git_submodules(self) -> None:
        """Verify git submodules are properly initialized"""
        print(f"\n{Colors.CYAN}🔗 Verifying Git Submodules{Colors.RESET}")
        
        submodules = [
            "zsh/zplug",
            "tmux/plugins/tpm"
        ]
        
        for submodule in submodules:
            self.total_checks += 1
            submodule_path = self.repo_path / submodule
            if submodule_path.exists() and (submodule_path / ".git").exists():
                self.success(f"{submodule} submodule initialized")
            else:
                self.error(f"{submodule} submodule not initialized")
    
    def verify_command_availability(self) -> None:
        """Verify essential commands are available in PATH"""
        print(f"\n{Colors.CYAN}🔍 Verifying Command Availability{Colors.RESET}")
        
        essential_commands = [
            "brew", "git", "zsh", "tmux", "nvim",
            "uv", "fnm", "go", "curl", "fzf", "rg"
        ]
        
        for cmd in essential_commands:
            self.total_checks += 1
            result = self.run_command(f"which {cmd}")
            if result and result.returncode == 0:
                self.success(f"{cmd} available in PATH")
            else:
                self.error(f"{cmd} not available in PATH")
    
    def generate_final_report(self) -> bool:
        """Generate final verification report"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 POST-INSTALLATION VERIFICATION REPORT{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        success_rate = (self.success_count / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print(f"\n📈 Overall Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}")
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Successful checks: {self.success_count}/{self.total_checks}")
        
        if not self.issues_found and not self.warnings_found:
            print(f"\n{Colors.GREEN}🎉 VERIFICATION PASSED!{Colors.RESET}")
            print("Your development environment is fully configured and ready to use.")
            return True
        else:
            if self.issues_found:
                print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] CRITICAL ISSUES ({len(self.issues_found)}){Colors.RESET}")
                for issue in self.issues_found:
                    print(f"  • {issue}")
            
            if self.warnings_found:
                print(f"\n{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]WARNINGS ({len(self.warnings_found)}){Colors.RESET}")
                for warning in self.warnings_found:
                    print(f"  • {warning}")
            
            print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] VERIFICATION FAILED!{Colors.RESET}")
            print("Please address the issues above before proceeding.")
            return False
    
    def run_full_verification(self) -> bool:
        """Run complete post-installation verification"""
        print(f"{Colors.BOLD}🔍 POST-INSTALLATION VERIFICATION{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        self.verify_essential_packages()
        self.verify_language_environments()
        self.verify_dotfiles_configuration()
        self.verify_neovim_setup()
        self.verify_git_submodules()
        self.verify_command_availability()
        
        return self.generate_final_report()


def main():
    """Main function"""
    verifier = PostInstallVerifier()
    success = verifier.run_full_verification()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()