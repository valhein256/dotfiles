#!/usr/bin/env python3
"""
Installation Verification Script
Comprehensive verification that all packages and configurations have been properly installed.
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


class InstallationVerifier:
    """Comprehensive installation verification system"""
    
    def __init__(self):
        self.home = Path.home()
        self.repo_path = Path.cwd()
        self.issues_found = []
        self.warnings_found = []
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
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def check_homebrew_packages(self) -> None:
        """Verify all essential Homebrew packages are installed"""
        print(f"\n{Colors.CYAN}🍺 Checking Homebrew Package Installation{Colors.RESET}")
        
        # Define essential packages by category
        essential_packages = {
            "Core Tools": ["zsh", "git", "tree", "fzf", "ripgrep"],
            "Editor": ["neovim", "universal-ctags"],
            "Terminal": ["tmux"],
            "Python": ["uv"],
            "Node.js": ["fnm", "pnpm"],
            "Go": ["go"],
            "Java Prerequisites": ["zip", "unzip", "curl"],
            "Rust": ["rustup-init"],
            "DevOps": ["kubectl", "helm", "terraform", "terragrunt"],
            "Cloud": ["awscli"],
            "Network": ["openssh", "sshs", "teleport"],
            "Fonts": ["font-sauce-code-pro-nerd-font"],
            "System": ["xquartz"],
        }
        
        total_packages = sum(len(packages) for packages in essential_packages.values())
        self.total_checks += total_packages
        
        for category, packages in essential_packages.items():
            print(f"\n🔍 Checking {category}:")
            for package in packages:
                # Check formulae first
                result = self.run_command(f"brew list {package}")
                if result and result.returncode == 0:
                    self.success(f"{package}")
                else:
                    # Check casks
                    result = self.run_command(f"brew list --cask {package}")
                    if result and result.returncode == 0:
                        self.success(f"{package} (cask)")
                    else:
                        self.error(f"{package} not installed")
    
    def check_language_environments(self) -> None:
        """Verify all language environments are properly set up"""
        print(f"\n{Colors.CYAN}🔧 Checking Language Environments{Colors.RESET}")
        
        # Python (uv)
        print(f"\n🐍 Python (uv):")
        self.total_checks += 2
        
        if self.run_command("which uv") and self.run_command("which uv").returncode == 0:
            self.success("uv command available")
            
            result = self.run_command("uv python list")
            if result and result.returncode == 0 and result.stdout.strip():
                python_versions = [line for line in result.stdout.split('\n') if 'cpython' in line.lower()]
                if python_versions:
                    self.success(f"Python versions installed ({len(python_versions)} found)")
                    # Show first few versions
                    for version in python_versions[:3]:
                        if version.strip():
                            print(f"    • {version.strip()}")
                else:
                    self.error("No Python versions installed via uv")
            else:
                self.error("uv installed but no Python versions found")
        else:
            self.error("uv not found")
            self.total_checks += 1  # Skip the second check
        
        # Node.js (fnm)
        print(f"\n🟢 Node.js (fnm):")
        self.total_checks += 2
        
        if self.run_command("which fnm") and self.run_command("which fnm").returncode == 0:
            self.success("fnm command available")
            
            result = self.run_command("fnm list")
            if result and result.returncode == 0:
                if "No Node.js versions installed" not in result.stdout:
                    self.success("Node.js versions installed")
                    # Show installed versions
                    for line in result.stdout.split('\n')[:5]:
                        if line.strip() and ('v' in line or 'system' in line):
                            print(f"    • {line.strip()}")
                else:
                    self.error("fnm installed but no Node.js versions found")
            else:
                self.error("fnm installed but cannot list versions")
        else:
            self.error("fnm not found")
            self.total_checks += 1  # Skip the second check
        
        # Java (SDKMAN)
        print(f"\n☕ Java (SDKMAN):")
        self.total_checks += 2
        
        sdkman_dir = self.home / ".sdkman"
        if sdkman_dir.exists():
            self.success("SDKMAN directory exists")
            
            java_dir = sdkman_dir / "candidates" / "java"
            if java_dir.exists():
                java_versions = [d.name for d in java_dir.iterdir() if d.is_dir() and d.name != "current"]
                if java_versions:
                    self.success(f"Java versions installed ({len(java_versions)} found)")
                    for version in java_versions:
                        print(f"    • {version}")
                else:
                    self.error("SDKMAN installed but no Java versions found")
            else:
                self.error("SDKMAN installed but no Java candidates directory")
        else:
            self.error("SDKMAN not installed")
            self.total_checks += 1  # Skip the second check
        
        # Rust
        print(f"\n🦀 Rust:")
        self.total_checks += 1
        
        result = self.run_command("rustc --version")
        if result and result.returncode == 0:
            self.success(f"Rust toolchain available: {result.stdout.strip()}")
        else:
            self.error("Rust toolchain not available")
        
        # Go
        print(f"\n🔵 Go:")
        self.total_checks += 1
        
        result = self.run_command("go version")
        if result and result.returncode == 0:
            self.success(f"Go available: {result.stdout.strip()}")
        else:
            self.error("Go not available")
    
    def check_dotfiles_configuration(self) -> None:
        """Verify all dotfiles are properly configured"""
        print(f"\n{Colors.CYAN}⚙️  Checking Dotfiles Configuration{Colors.RESET}")
        
        expected_symlinks = [
            (self.home / ".zshrc", "zsh/zshrc", "zsh configuration"),
            (self.home / ".gitconfig", "gitconfig", "git configuration"),
            (self.home / ".tmux.conf", "tmux/tmux.conf", "tmux configuration"),
            (self.home / ".screenrc", "screenrc", "screen configuration"),
            (self.home / ".ssh" / "rc", "sshrc", "ssh configuration"),
            (self.home / ".tmux", "tmux", "tmux directory"),
            (self.home / ".zplug", "zsh/zplug", "zplug directory"),
            (self.home / ".tools", "tools", "tools directory"),
        ]
        
        self.total_checks += len(expected_symlinks)
        
        for home_path, repo_path, description in expected_symlinks:
            if home_path.exists() and home_path.is_symlink():
                target = home_path.resolve()
                expected_target = self.repo_path / repo_path
                if target == expected_target:
                    self.success(f"{description} correctly symlinked")
                else:
                    self.error(f"{description} symlinked to wrong target: {target}")
            else:
                self.error(f"{description} not properly symlinked")
    
    def check_neovim_setup(self) -> None:
        """Verify Neovim is properly set up"""
        print(f"\n{Colors.CYAN}📝 Checking Neovim Setup{Colors.RESET}")
        
        # Check Neovim symlink
        self.total_checks += 1
        nvim_config = self.home / ".config" / "nvim"
        if nvim_config.exists() and nvim_config.is_symlink():
            target = nvim_config.resolve()
            expected_target = self.repo_path / "neovim"
            if target == expected_target:
                self.success("Neovim config correctly symlinked")
            else:
                self.error(f"Neovim config symlinked to wrong target: {target}")
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
        
        # Check plugins directory
        self.total_checks += 1
        # Check both possible plugin locations
        plugged_dir_repo = self.repo_path / "neovim" / "plugged"
        plugged_dir_system = self.home / ".local" / "share" / "nvim" / "plugged"
        
        plugin_count = 0
        plugin_location = ""
        
        if plugged_dir_system.exists():
            plugin_count = len([d for d in plugged_dir_system.iterdir() if d.is_dir()])
            plugin_location = "~/.local/share/nvim/plugged"
        elif plugged_dir_repo.exists():
            plugin_count = len([d for d in plugged_dir_repo.iterdir() if d.is_dir()])
            plugin_location = "dotfiles/neovim/plugged"
        
        if plugin_count > 0:
            self.success(f"Neovim plugins installed ({plugin_count} plugins in {plugin_location})")
        else:
            self.warning("No Neovim plugins found - run :PlugInstall in nvim")
        
        # Check Neovim command availability
        self.total_checks += 1
        result = self.run_command("nvim --version")
        if result and result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            self.success(f"Neovim command available: {version_line}")
        else:
            self.error("Neovim command not available")
    
    def check_git_submodules(self) -> None:
        """Verify git submodules are properly initialized"""
        print(f"\n{Colors.CYAN}🔗 Checking Git Submodules{Colors.RESET}")
        
        submodules = [
            ("zsh/zplug", "zplug submodule"),
            ("tmux/plugins/tpm", "tmux plugin manager"),
        ]
        
        self.total_checks += len(submodules)
        
        for submodule_path, description in submodules:
            submodule_full_path = self.repo_path / submodule_path
            if submodule_full_path.exists() and (submodule_full_path / ".git").exists():
                self.success(f"{description} initialized")
            else:
                self.error(f"{description} not initialized")
    
    def check_command_availability(self) -> None:
        """Verify essential commands are available in PATH"""
        print(f"\n{Colors.CYAN}🔍 Checking Command Availability{Colors.RESET}")
        
        essential_commands = [
            ("brew", "Homebrew package manager"),
            ("git", "Version control system"),
            ("zsh", "Z shell"),
            ("tmux", "Terminal multiplexer"),
            ("nvim", "Neovim editor"),
            ("uv", "Python package manager"),
            ("fnm", "Node.js version manager"),
            ("go", "Go programming language"),
            ("curl", "Download tool"),
            ("fzf", "Fuzzy finder"),
            ("rg", "Ripgrep search tool"),
        ]
        
        self.total_checks += len(essential_commands)
        
        for cmd, description in essential_commands:
            result = self.run_command(f"which {cmd}")
            if result and result.returncode == 0:
                self.success(f"{cmd} available - {description}")
            else:
                self.error(f"{cmd} not available - {description}")
    
    def check_development_environment(self) -> None:
        """Verify development environment is ready"""
        print(f"\n{Colors.CYAN}🚀 Checking Development Environment Readiness{Colors.RESET}")
        
        # Test Python environment
        self.total_checks += 1
        result = self.run_command("uv python list")
        if result and result.returncode == 0 and "cpython" in result.stdout.lower():
            self.success("Python development environment ready")
        else:
            self.error("Python development environment not ready")
        
        # Test Node.js environment
        self.total_checks += 1
        result = self.run_command("fnm current")
        if result and result.returncode == 0:
            self.success("Node.js development environment ready")
        else:
            self.error("Node.js development environment not ready")
        
        # Test Java environment
        self.total_checks += 1
        java_check = f"source {self.home}/.sdkman/bin/sdkman-init.sh && java -version"
        result = self.run_command(java_check)
        if result and result.returncode == 0:
            self.success("Java development environment ready")
        else:
            self.warning("Java development environment may need manual activation")
        
        # Test Rust environment
        self.total_checks += 1
        result = self.run_command("cargo --version")
        if result and result.returncode == 0:
            self.success("Rust development environment ready")
        else:
            self.error("Rust development environment not ready")
        
        # Test Go environment
        self.total_checks += 1
        result = self.run_command("go version")
        if result and result.returncode == 0:
            self.success("Go development environment ready")
        else:
            self.error("Go development environment not ready")
    
    def generate_installation_report(self) -> bool:
        """Generate comprehensive installation verification report"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 INSTALLATION VERIFICATION REPORT{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*60}{Colors.RESET}")
        
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print(f"\n📈 Installation Success Rate: {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}")
        print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Successful installations: {self.passed_checks}/{self.total_checks}")
        
        if not self.issues_found and not self.warnings_found:
            print(f"\n{Colors.GREEN}🎉 INSTALLATION VERIFICATION PASSED!{Colors.RESET}")
            print("Your development environment is fully configured and ready to use!")
            
            print(f"\n{Colors.CYAN}🚀 Quick Start Commands:{Colors.RESET}")
            print("  # Python development")
            print("  uv python list                    # List installed Python versions")
            print("  uv venv                           # Create virtual environment")
            print("  uv pip install package           # Install Python packages")
            print()
            print("  # Node.js development")
            print("  fnm list                          # List installed Node.js versions")
            print("  fnm use 18                        # Switch to Node.js 18")
            print("  npm install -g package            # Install global packages")
            print()
            print("  # Java development")
            print("  source ~/.sdkman/bin/sdkman-init.sh")
            print("  sdk list java                     # List available JDKs")
            print("  sdk use java 21.0.1-tem         # Switch to Java 21")
            print()
            print("  # Development tools")
            print("  nvim                              # Start Neovim")
            print("  tmux                              # Start terminal multiplexer")
            print("  fzf                               # Fuzzy finder")
            print("  rg 'pattern'                      # Search with ripgrep")
            
            return True
        else:
            if self.issues_found:
                print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] INSTALLATION ISSUES FOUND ({len(self.issues_found)}){Colors.RESET}")
                print("The following components are not properly installed:")
                for issue in self.issues_found:
                    print(f"  • {issue}")
                
                print(f"\n{Colors.YELLOW}💡 Fix Commands:{Colors.RESET}")
                print("  # Reinstall missing packages:")
                print("  make packages")
                print()
                print("  # Reinstall language managers:")
                print("  make language-managers")
                print()
                print("  # Reinstall dotfiles:")
                print("  make dotfiles")
                print()
                print("  # Reinstall Neovim setup:")
                print("  make neovim-plugins")
            
            if self.warnings_found:
                print(f"\n{Colors.YELLOW}[ {Colors.YELLOW}WARN{Colors.RESET} ]WARNINGS ({len(self.warnings_found)}){Colors.RESET}")
                for warning in self.warnings_found:
                    print(f"  • {warning}")
            
            print(f"\n{Colors.RED}[ {Colors.RED}FAIL{Colors.RESET} ] INSTALLATION VERIFICATION FAILED!{Colors.RESET}")
            print("Please address the issues above to complete your development environment setup.")
            return False
    
    def run_full_installation_verification(self) -> bool:
        """Run complete installation verification"""
        print(f"{Colors.BOLD}🔍 INSTALLATION VERIFICATION{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        print("Verifying that all packages and configurations have been properly installed...")
        
        self.check_homebrew_packages()
        self.check_language_environments()
        self.check_dotfiles_configuration()
        self.check_neovim_setup()
        self.check_git_submodules()
        self.check_command_availability()
        self.check_development_environment()
        
        return self.generate_installation_report()


def main():
    """Main function"""
    verifier = InstallationVerifier()
    success = verifier.run_full_installation_verification()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()