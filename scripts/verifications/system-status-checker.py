#!/usr/bin/env python3
"""
System Status Checker
Comprehensive verification of system cleanup and package status with parallel processing
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time


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


class CheckResult:
    """Container for check results"""
    def __init__(self, name: str, success: bool = True):
        self.name = name
        self.success = success
        self.messages = []
        self.warnings = []
        self.errors = []
        self.info_messages = []
    
    def add_success(self, message: str):
        self.messages.append(('success', message))
    
    def add_warning(self, message: str):
        self.messages.append(('warning', message))
        self.warnings.append(message)
        
    def add_error(self, message: str):
        self.messages.append(('error', message))
        self.errors.append(message)
        self.success = False
        
    def add_info(self, message: str):
        self.messages.append(('info', message))
        self.info_messages.append(message)


class SystemStatusChecker:
    """Comprehensive system status checker with parallel processing"""
    
    def __init__(self, check_type: str = 'installed'):
        self.home = Path.home()
        self.output_lock = threading.Lock()
        self.all_results = []
        self.check_type = check_type  # 'cleaned' or 'installed'
    
    def run_command(self, cmd: str, capture_output: bool = True) -> Optional[subprocess.CompletedProcess]:
        """Run a command and return the result"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
            return result
        except Exception:
            return None
    
    def print_result(self, result: CheckResult):
        """Print the results of a check"""
        with self.output_lock:
            # Print section header
            print(f"\n{Colors.CYAN}{Colors.BOLD}{result.name}{Colors.RESET}")
            
            for msg_type, message in result.messages:
                if msg_type == 'success':
                    print(f"  [{Colors.GREEN}  OK  {Colors.RESET}] {message}")
                elif msg_type == 'warning':
                    print(f"  [{Colors.YELLOW} WARN {Colors.RESET}] {message}")
                elif msg_type == 'error':
                    print(f"  [{Colors.RED} FAIL {Colors.RESET}] {message}")
                elif msg_type == 'info':
                    print(f"  [{Colors.BLUE} INFO {Colors.RESET}] {message}")
    
    def check_homebrew_packages(self) -> CheckResult:
        """Check Homebrew package status"""
        result = CheckResult("📦 Homebrew Packages")
        
        total_packages = 0
        
        # Check formulae
        result.add_info("🍺 Homebrew formulae:")
        cmd_result = self.run_command("brew list --formula")
        if cmd_result and cmd_result.returncode == 0:
            formulae = cmd_result.stdout.strip().split('\n') if cmd_result.stdout.strip() else []
            formulae_count = len([f for f in formulae if f.strip()])
            total_packages += formulae_count
            if formulae_count > 0:
                if self.check_type == 'cleaned':
                    result.add_warning(f"  • {formulae_count} formulae installed - Needs cleanup")
                else:  # installed
                    result.add_success(f"  • {formulae_count} formulae installed - Available")
                # Show first few packages
                for formula in formulae[:5]:
                    if formula.strip():
                        result.add_info(f"    • {formula.strip()}")
                if formulae_count > 5:
                    result.add_info(f"    • ... and {formulae_count - 5} more")
            else:
                if self.check_type == 'cleaned':
                    result.add_success("  • No formulae installed - Clean")
                else:  # installed
                    result.add_warning("  • No formulae installed - Needs installation")
        
        # Check casks
        result.add_info("📦 Homebrew casks:")
        cmd_result = self.run_command("brew list --cask")
        if cmd_result and cmd_result.returncode == 0:
            casks = cmd_result.stdout.strip().split('\n') if cmd_result.stdout.strip() else []
            casks_count = len([c for c in casks if c.strip()])
            total_packages += casks_count
            if casks_count > 0:
                if self.check_type == 'cleaned':
                    result.add_warning(f"  • {casks_count} casks installed - Needs cleanup")
                else:  # installed
                    result.add_success(f"  • {casks_count} casks installed - Available")
                # Show first few packages
                for cask in casks[:5]:
                    if cask.strip():
                        result.add_info(f"    • {cask.strip()}")
                if casks_count > 5:
                    result.add_info(f"    • ... and {casks_count - 5} more")
            else:
                if self.check_type == 'cleaned':
                    result.add_success("  • No casks installed - Clean")
                else:  # installed
                    result.add_warning("  • No casks installed - Needs installation")
        
        # Check taps
        result.add_info("🚰 Homebrew taps:")
        cmd_result = self.run_command("brew tap")
        if cmd_result and cmd_result.returncode == 0:
            taps = cmd_result.stdout.strip().split('\n') if cmd_result.stdout.strip() else []
            custom_taps = [tap for tap in taps if tap.strip() and not tap.startswith('homebrew/')]
            if custom_taps:
                if self.check_type == 'cleaned':
                    result.add_warning(f"  • {len(custom_taps)} custom taps installed - Needs cleanup")
                else:  # installed
                    result.add_success(f"  • {len(custom_taps)} custom taps installed - Available")
                for tap in custom_taps:
                    result.add_info(f"    • {tap}")
            else:
                if self.check_type == 'cleaned':
                    result.add_success("  • No custom taps installed - Clean")
                else:  # installed
                    result.add_warning("  • No custom taps installed - Needs installation")
        
        # Generate summary
        if total_packages == 0:
            if self.check_type == 'cleaned':
                result.add_info("📋 Summary: All clean (0 packages)")
            else:  # installed
                result.add_info("📋 Summary: No packages installed (needs installation)")
        else:
            if self.check_type == 'cleaned':
                result.add_info(f"📋 Summary: {total_packages} total packages installed (needs cleanup)")
            else:  # installed
                result.add_info(f"📋 Summary: {total_packages} total packages installed")
        
        return result
    
    def check_language_managers(self) -> CheckResult:
        """Check language version managers"""
        result = CheckResult("🔧 Language Managers")
        
        installed_count = 0
        
        # Python (uv)
        result.add_info("🐍 Python (uv) directories:")
        uv_data = self.home / ".local" / "share" / "uv"
        uv_cache = self.home / ".cache" / "uv"
        
        if uv_data.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {uv_data} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {uv_data} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {uv_data} - Clean")
            else:  # installed
                result.add_warning(f"  • {uv_data} - Needs installation")
            
        if uv_cache.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {uv_cache} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {uv_cache} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {uv_cache} - Clean")
            else:  # installed
                result.add_warning(f"  • {uv_cache} - Needs installation")
        
        # Node.js (fnm)
        result.add_info("🟢 Node.js (fnm) directories:")
        fnm_dir = self.home / ".local" / "share" / "fnm"
        fnm_alt = self.home / ".fnm"
        
        if fnm_dir.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {fnm_dir} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {fnm_dir} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {fnm_dir} - Clean")
            else:  # installed
                # Check if fnm is working even without this directory
                fnm_result = self.run_command("fnm list")
                if fnm_result and fnm_result.returncode == 0:
                    result.add_success(f"  • {fnm_dir} - Not needed (fnm working via alternative path)")
                else:
                    result.add_warning(f"  • {fnm_dir} - Needs installation")
            
        if fnm_alt.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {fnm_alt} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {fnm_alt} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {fnm_alt} - Clean")
            else:  # installed
                # This directory is optional - fnm can work without it
                result.add_success(f"  • {fnm_alt} - Clean (optional directory)")
        
        
        # Java (SDKMAN)
        result.add_info("☕ Java (SDKMAN) directories:")
        sdkman_dir = self.home / ".sdkman"
        
        if sdkman_dir.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {sdkman_dir} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {sdkman_dir} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {sdkman_dir} - Clean")
            else:  # installed
                result.add_warning(f"  • {sdkman_dir} - Needs installation")
        
        # Rust (rustup/cargo)
        result.add_info("🦀 Rust directories:")
        rustup_dir = self.home / ".rustup"
        cargo_dir = self.home / ".cargo"
        
        if rustup_dir.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {rustup_dir} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {rustup_dir} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {rustup_dir} - Clean")
            else:  # installed
                result.add_warning(f"  • {rustup_dir} - Needs installation")
            
        if cargo_dir.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {cargo_dir} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {cargo_dir} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {cargo_dir} - Clean")
            else:  # installed
                result.add_warning(f"  • {cargo_dir} - Needs installation")
        
        # Go
        result.add_info("🔵 Go directories:")
        go_path = self.home / "go"
        go_cache = self.home / ".cache" / "go-build"
        
        if go_path.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {go_path} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {go_path} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {go_path} - Clean")
            else:  # installed
                result.add_warning(f"  • {go_path} - Needs installation")
            
        if go_cache.exists():
            if self.check_type == 'cleaned':
                result.add_warning(f"  • {go_cache} - EXISTS - Needs cleanup")
            else:  # installed
                result.add_success(f"  • {go_cache} - Available")
            installed_count += 1
        else:
            if self.check_type == 'cleaned':
                result.add_success(f"  • {go_cache} - Clean")
            else:  # installed
                # Go build cache is created automatically when needed
                result.add_success(f"  • {go_cache} - Clean (created automatically when needed)")
        
        # Generate summary
        if installed_count == 0:
            if self.check_type == 'cleaned':
                result.add_info("📋 Summary: All clean (0 directories found)")
            else:  # installed
                result.add_info("📋 Summary: No language managers installed (needs installation)")
        else:
            if self.check_type == 'cleaned':
                result.add_info(f"📋 Summary: {installed_count} directories found (needs cleanup)")
            else:  # installed
                result.add_info(f"📋 Summary: {installed_count} directories found")
        
        return result
    
    def check_dependency_packages(self) -> CheckResult:
        """Check if all dependency packages are properly installed"""
        result = CheckResult("📦 Checking Dependency Packages")
        
        # Define essential packages by category
        essential_packages = {
            "core": ["zsh", "git", "tree", "fzf", "ripgrep"],
            "editor": ["neovim", "universal-ctags"],
            "terminal": ["tmux"],
            "python": ["uv"],
            "nodejs": ["fnm", "pnpm"],
            "golang": ["go"],
            "java-prereq": ["zip", "unzip", "curl"],
            "rust": ["rustup-init"],
            "devops": ["kubectl", "helm", "terraform", "terragrunt"],
            "cloud": ["awscli"],
            "network": ["openssh", "sshs", "teleport"],
        }
        
        installed_packages = []
        missing_packages = []
        
        for category, packages in essential_packages.items():
            result.add_info(f"🔍 {category.title()} packages:")
            for package in packages:
                cmd_result = self.run_command(f"brew list {package}")
                if cmd_result and cmd_result.returncode == 0:
                    result.add_success(f"  • {package} - Available")
                    installed_packages.append(f"{category}/{package}")
                else:
                    result.add_success(f"  • {package} - Clean")
                    missing_packages.append(f"{category}/{package}")
        
        # Generate summary
        total_packages = len(installed_packages) + len(missing_packages)
        if len(installed_packages) == 0:
            result.add_info(f"📋 Summary: All clean ({len(installed_packages)}/{total_packages} available)")
        else:
            result.add_info(f"📋 Summary: {len(installed_packages)}/{total_packages} installed")
        
        return result
    
    def check_language_environments(self) -> CheckResult:
        """Check language version managers and their installations"""
        result = CheckResult("🔧 Checking Language Environments")
        
        installed_count = 0
        
        # Python (uv)
        result.add_info("🐍 Python (uv) manager and versions:")
        uv_cmd = self.run_command("which uv")
        if uv_cmd and uv_cmd.returncode == 0:
            uv_path = uv_cmd.stdout.strip()
            result.add_success(f"  • uv command - Available: {uv_path}")
            
            cmd_result = self.run_command("uv python list")
            if cmd_result and cmd_result.returncode == 0:
                python_versions = [line.strip() for line in cmd_result.stdout.split('\n') if line.strip()]
                if python_versions:
                    installed_count += 1
                    result.add_success(f"  • Python versions - {len(python_versions)} installed")
                    for version in python_versions[:3]:  # Show first 3
                        result.add_info(f"    • {version}")
                    if len(python_versions) > 3:
                        result.add_info(f"    • ... and {len(python_versions) - 3} more")
                else:
                    result.add_success("  • Python versions - None installed")
            else:
                result.add_success("  • Python versions - Cannot list versions")
        else:
            result.add_success("  • uv command - Clean")
            result.add_success("  • Python versions - Clean")
        
        # Node.js (fnm)
        result.add_info("🟢 Node.js (fnm) manager and versions:")
        fnm_cmd = self.run_command("which fnm")
        if fnm_cmd and fnm_cmd.returncode == 0:
            fnm_path = fnm_cmd.stdout.strip()
            result.add_success(f"  • fnm command - Available: {fnm_path}")
            
            cmd_result = self.run_command("fnm list")
            if cmd_result and cmd_result.returncode == 0:
                if "No Node.js versions installed" not in cmd_result.stdout:
                    node_versions = [line.strip() for line in cmd_result.stdout.split('\n') if line.strip()]
                    installed_count += 1
                    result.add_success(f"  • Node.js versions - {len(node_versions)} installed")
                    # Show installed versions
                    for line in cmd_result.stdout.split('\n')[:3]:
                        if line.strip():
                            result.add_info(f"    • {line.strip()}")
                    if len(node_versions) > 3:
                        result.add_info(f"    • ... and {len(node_versions) - 3} more")
                else:
                    result.add_success("  • Node.js versions - None installed")
            else:
                result.add_success("  • Node.js versions - Cannot list versions")
        else:
            result.add_success("  • fnm command - Clean")
            result.add_success("  • Node.js versions - Clean")
        
        # Java (SDKMAN)
        result.add_info("☕ Java (SDKMAN) manager and versions:")
        sdkman_dir = self.home / ".sdkman"
        if sdkman_dir.exists():
            result.add_success(f"  • SDKMAN directory - Available: {sdkman_dir}")
            
            # Check for Java installations
            java_dir = sdkman_dir / "candidates" / "java"
            if java_dir.exists():
                java_versions = [d.name for d in java_dir.iterdir() if d.is_dir() and d.name != "current"]
                if java_versions:
                    installed_count += 1
                    result.add_success(f"  • Java versions - {len(java_versions)} installed")
                    for version in java_versions:
                        result.add_info(f"    • {version}")
                else:
                    result.add_success("  • Java versions - None installed")
            else:
                result.add_success("  • Java versions - No candidates directory")
        else:
            result.add_success("  • SDKMAN directory - Clean")
            result.add_success("  • Java versions - Clean")
        
        # Rust
        result.add_info("🦀 Rust toolchain:")
        cargo_dir = self.home / ".cargo"
        rustc_cmd = self.run_command("rustc --version")
        
        if cargo_dir.exists():
            result.add_success(f"  • Cargo directory - Available: {cargo_dir}")
        else:
            result.add_success("  • Cargo directory - Clean")
            
        if rustc_cmd and rustc_cmd.returncode == 0:
            installed_count += 1
            result.add_success(f"  • Rust compiler - {rustc_cmd.stdout.strip()}")
        else:
            result.add_success("  • Rust compiler - Clean")
        
        # Go
        result.add_info("🔵 Go toolchain:")
        go_cmd = self.run_command("go version")
        go_path = self.home / "go"
        
        if go_cmd and go_cmd.returncode == 0:
            installed_count += 1
            go_version = go_cmd.stdout.strip()
            which_go = self.run_command("which go")
            if which_go and which_go.returncode == 0:
                go_binary_path = which_go.stdout.strip()
                result.add_success(f"  • Go compiler - {go_version}")
                result.add_info(f"    • Binary location: {go_binary_path}")
            else:
                result.add_success(f"  • Go compiler - {go_version}")
        else:
            result.add_success("  • Go compiler - Clean")
            
        if go_path.exists():
            result.add_success(f"  • Go workspace - Available: {go_path}")
        else:
            result.add_success("  • Go workspace - Not created")
        
        # Generate summary
        if installed_count == 0:
            result.add_info("📋 Summary: All clean (0 available)")
        else:
            result.add_info(f"📋 Summary: {installed_count} installed")
        
        return result
    
    def check_neovim_status(self) -> CheckResult:
        """Check Neovim status - system data, config links, and dynamic content"""
        result = CheckResult("📝 Checking Neovim Status")
        
        # Check system-wide neovim directories (user data and cache)
        system_neovim_dirs = [
            self.home / ".local" / "share" / "nvim",  # Neovim data directory
            self.home / ".cache" / "nvim",            # Neovim cache directory
            self.home / ".vim" / "plugged",           # Vim plugins directory
            self.home / ".vim" / "autoload"           # Vim autoload directory
        ]
        
        # Check dotfiles neovim dynamic content (auto-generated files)
        dotfiles_dynamic_dirs = [
            Path("neovim/plugged"),           # Plugin installation directory
            Path("neovim/env")                # Environment files directory
        ]
        
        dotfiles_dynamic_files = [
            Path("neovim/autoload/plug.vim")  # Plugin manager file
        ]
        
        # Check ~/.config/nvim status (configuration symlink)
        nvim_config = self.home / ".config" / "nvim"
        
        # 1. Check system directories (user data and cache that should be cleaned)
        result.add_info("🔍 System Neovim directories (user data/cache):")
        for d in system_neovim_dirs:
            if d.exists():
                if self.check_type == 'cleaned':
                    result.add_warning(f"  • {d} - EXISTS (needs cleanup)")
                else:  # installed
                    result.add_success(f"  • {d} - Available (user data)")
            else:
                if self.check_type == 'cleaned':
                    result.add_success(f"  • {d} - Clean")
                else:  # installed
                    result.add_success(f"  • {d} - Clean")
        
        # Summary for system directories
        remaining_system_dirs = [d for d in system_neovim_dirs if d.exists()]
        if remaining_system_dirs:
            result.add_info(f"📋 Summary: {len(remaining_system_dirs)}/{len(system_neovim_dirs)} directories found (user data/cache)")
        else:
            result.add_info("📋 Summary: All clean (0 directories found)")
        
        # 2. Check ~/.config/nvim status (configuration symlink state)
        result.add_info("🔗 Neovim config symlink:")
        
        if nvim_config.exists():
            if nvim_config.is_symlink():
                target = nvim_config.resolve()
                dotfiles_neovim = Path.cwd() / "neovim"
                if target == dotfiles_neovim:
                    result.add_success(f"  • {nvim_config} - Correctly linked to dotfiles")
                else:
                    result.add_warning(f"  • {nvim_config} - Wrong link target: {target}")
            else:
                result.add_warning(f"  • {nvim_config} - Directory exists (not symlinked)")
        else:
            result.add_success(f"  • {nvim_config} - Clean")
        
        result.add_info("📋 Summary: Clean")
        
        # 3. Check dotfiles dynamic content (auto-generated files in repo)
        result.add_info("📁 Dotfiles dynamic content (auto-generated in repo):")
        
        # Check directories
        for d in dotfiles_dynamic_dirs:
            if d.exists():
                result.add_info(f"  • {d}/ - EXISTS (auto-generated)")
            else:
                result.add_success(f"  • {d}/ - Clean")
        
        # Check files
        for f in dotfiles_dynamic_files:
            if f.exists():
                result.add_info(f"  • {f} - EXISTS (auto-generated)")
            else:
                result.add_success(f"  • {f} - Clean")
        
        # Summary for dynamic content
        remaining_dynamic_dirs = [d for d in dotfiles_dynamic_dirs if d.exists()]
        remaining_dynamic_files = [f for f in dotfiles_dynamic_files if f.exists()]
        
        total_dynamic = len(remaining_dynamic_dirs) + len(remaining_dynamic_files)
        total_possible = len(dotfiles_dynamic_dirs) + len(dotfiles_dynamic_files)
        
        if remaining_dynamic_dirs or remaining_dynamic_files:
            result.add_info(f"📋 Summary: {total_dynamic}/{total_possible} files found (auto-generated)")
        else:
            result.add_info("📋 Summary: All clean (0 files found)")
        
        return result
    
    def check_dotfiles_status(self) -> CheckResult:
        """Check dotfiles symlink status - managed configuration files and directories"""
        result = CheckResult("⚙️  Checking Dotfiles Status")
        
        # Define all dotfiles that should be managed by this repo
        managed_dotfiles = [
            (self.home / ".zshrc", "zsh/zshrc"),           # Zsh configuration
            (self.home / ".gitconfig", "gitconfig"),       # Git configuration
            (self.home / ".tmux.conf", "tmux/tmux.conf"),  # Tmux configuration
            (self.home / ".screenrc", "screenrc"),         # Screen configuration
            (self.home / ".ssh" / "rc", "sshrc"),          # SSH configuration
        ]
        
        # Define directories that should be managed
        managed_directories = [
            (self.home / ".tmux", "tmux"),           # Tmux plugins and scripts
            (self.home / ".zplug", "zsh/zplug"),     # Zsh plugin manager
            (self.home / ".tools", "tools"),         # Custom tools directory
        ]
        
        # Check managed dotfiles
        result.add_info("📄 Managed dotfiles (symlink status):")
        dotfiles_installed = 0
        for home_path, repo_path in managed_dotfiles:
            expected_target = Path.cwd() / repo_path
            
            if home_path.exists():
                if home_path.is_symlink():
                    target = home_path.resolve()
                    if target == expected_target:
                        result.add_success(f"  • {home_path} → {repo_path} - Correctly linked")
                        dotfiles_installed += 1
                    else:
                        result.add_warning(f"  • {home_path} → {target} - Wrong target")
                        dotfiles_installed += 1
                else:
                    result.add_warning(f"  • {home_path} - File exists (not symlinked)")
                    dotfiles_installed += 1
            else:
                result.add_success(f"  • {home_path} → {repo_path} - Clean")
        
        # Summary for dotfiles
        if dotfiles_installed == 0:
            result.add_info(f"📋 Summary: All clean ({dotfiles_installed}/{len(managed_dotfiles)} available)")
        else:
            result.add_info(f"📋 Summary: {dotfiles_installed}/{len(managed_dotfiles)} installed")
        
        # Check managed directories
        result.add_info("📁 Managed directories (symlink status):")
        directories_installed = 0
        for home_path, repo_path in managed_directories:
            expected_target = Path.cwd() / repo_path
            
            if home_path.exists():
                if home_path.is_symlink():
                    target = home_path.resolve()
                    if target == expected_target:
                        result.add_success(f"  • {home_path} → {repo_path} - Correctly linked")
                        directories_installed += 1
                    else:
                        result.add_warning(f"  • {home_path} → {target} - Wrong target")
                        directories_installed += 1
                else:
                    result.add_warning(f"  • {home_path} - Directory exists (not symlinked)")
                    directories_installed += 1
            else:
                result.add_success(f"  • {home_path} → {repo_path} - Clean")
        
        # Summary for directories
        if directories_installed == 0:
            result.add_info(f"📋 Summary: All clean ({directories_installed}/{len(managed_directories)} available)")
        else:
            result.add_info(f"📋 Summary: {directories_installed}/{len(managed_directories)} installed")
        
        return result
        return result
    
    def check_system_commands(self) -> CheckResult:
        """Check if system commands are available"""
        result = CheckResult("🔍 Checking System Commands")
        
        essential_commands = [
            ("brew", "Homebrew package manager"),
            ("git", "Version control system"),
            ("curl", "Download tool"),
            ("zsh", "Z shell")
        ]
        
        result.add_info("⚙️  Essential system commands:")
        available_count = 0
        
        for cmd, description in essential_commands:
            cmd_result = self.run_command(f"which {cmd}")
            if cmd_result and cmd_result.returncode == 0:
                cmd_path = cmd_result.stdout.strip()
                result.add_success(f"  • {cmd} - Available: {cmd_path}")
                available_count += 1
            else:
                result.add_error(f"  • {cmd} - NOT FOUND ({description})")
        
        # Generate summary
        if available_count == len(essential_commands):
            result.add_info(f"📋 Summary: All available ({available_count}/{len(essential_commands)})")
        else:
            missing_count = len(essential_commands) - available_count
            result.add_info(f"📋 Summary: {missing_count} missing, {available_count} available")
        
        return result
    
    def check_local_taps(self) -> CheckResult:
        """Check local tap status"""
        result = CheckResult("🏠 Checking Local Taps")
        
        cmd_result = self.run_command("brew tap")
        if cmd_result and cmd_result.returncode == 0:
            taps = cmd_result.stdout.strip().split('\n') if cmd_result.stdout.strip() else []
            local_taps = [tap for tap in taps if 'local/' in tap]
            
            result.add_info("🔍 Local tap directories:")
            
            if local_taps:
                for tap in local_taps:
                    if self.check_type == 'cleaned':
                        result.add_warning(f"  • {tap} - INSTALLED")
                    else:  # installed
                        result.add_success(f"  • {tap} - Available")
                    
                    # Check if tap has formulas
                    tap_path = Path(f"/opt/homebrew/Library/Taps/{tap.replace('/', '/homebrew-')}")
                    formula_dir = tap_path / "Formula"
                    if formula_dir.exists():
                        formulas = list(formula_dir.glob("*.rb"))
                        if formulas:
                            result.add_info(f"      📋 Formulas ({len(formulas)}):")
                            for formula in formulas:
                                result.add_info(f"     • {formula.stem}")
                        else:
                            result.add_info(f"      📋 No formulas found")
                    else:
                        result.add_info(f"      📋 No Formula directory")
                
                if self.check_type == 'cleaned':
                    result.add_info(f"📋 Summary: {len(local_taps)} installed")
                else:  # installed
                    result.add_info(f"📋 Summary: {len(local_taps)} installed")
            else:
                if self.check_type == 'cleaned':
                    result.add_success("  • No local taps found - Clean")
                else:  # installed
                    result.add_success("  • No local taps found - Clean")
                result.add_info("📋 Summary: All clean (0 found)")
        else:
            result.add_warning("Could not check taps status (brew tap failed)")
        
        return result
    
    def generate_summary(self, results: List[CheckResult]) -> bool:
        """Generate summary report"""
        print(f"\n{Colors.BOLD}{'='*50}{Colors.RESET}")
        print(f"{Colors.BOLD}📊 SUMMARY{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        
        all_errors = []
        all_warnings = []
        warnings_by_category = {}
        
        for result in results:
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            
            # Group warnings by category
            if result.warnings:
                category_name = result.name
                warnings_by_category[category_name] = result.warnings
        
        # Show status based on check type
        if all_errors:
            print(f"\n[{Colors.RED} FAIL {Colors.RESET}] {len(all_errors)} issue(s) found")
            for error in all_errors:
                print(f"  • {error}")
        elif all_warnings:
            print(f"\n[{Colors.YELLOW} WARN {Colors.RESET}] {len(all_warnings)} warning(s) found:")
            for category_name, warnings in warnings_by_category.items():
                print(f"{category_name}")
                for warning in warnings:
                    print(f"{warning}")
        else:
            if self.check_type == 'cleaned':
                print(f"\n[{Colors.GREEN}  OK  {Colors.RESET}] System is clean")
            else:  # installed
                print(f"\n[{Colors.GREEN}  OK  {Colors.RESET}] Development environment is properly installed")
        
        # Show next steps based on check type and status
        if all_errors:
            print(f"\n🔧 Run cleanup commands to fix issues")
        elif all_warnings:
            if self.check_type == 'cleaned':
                print(f"\n🧹 Run 'make clean' to remove all packages")
            else:  # installed
                print(f"\n🔧 Run installation commands to fix missing components")
        else:
            if self.check_type == 'cleaned':
                print(f"\n🚀 Run 'make install' to set up development environment")
            else:  # installed
                print(f"\n✅ System is ready for development")
        
        return len(all_errors) == 0
    
    def run_parallel_check(self, max_workers: int = 4) -> bool:
        """Run all checks in parallel"""
        print(f"{Colors.BOLD}🔍 SYSTEM STATUS CHECKER{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        print(f"{Colors.BLUE}Running checks with {max_workers} parallel workers...{Colors.RESET}")
        
        # Define all check functions
        check_functions = [
            self.check_homebrew_packages,
            self.check_dependency_packages,
            self.check_language_managers,
            self.check_language_environments,
            self.check_neovim_status,
            self.check_dotfiles_status,
            self.check_system_commands,
            self.check_local_taps,
        ]
        
        results = []
        start_time = time.time()
        
        # Execute checks in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_check = {executor.submit(check_func): check_func.__name__ for check_func in check_functions}
            
            # Collect results as they complete
            for future in as_completed(future_to_check):
                check_name = future_to_check[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.print_result(result)
                except Exception as exc:
                    error_result = CheckResult(f"[ {Colors.RED}FAIL{Colors.RESET} ] {check_name}")
                    error_result.add_error(f"Check failed with exception: {exc}")
                    results.append(error_result)
                    self.print_result(error_result)
        
        end_time = time.time()
        
        print(f"\n{Colors.BLUE}All checks completed in {end_time - start_time:.2f} seconds{Colors.RESET}")
        
        # Generate summary
        success = self.generate_summary(results)
        
        return success
    
    def run_sequential_check(self) -> bool:
        """Run all checks sequentially (fallback)"""
        print(f"{Colors.BOLD}🔍 SYSTEM STATUS CHECKER{Colors.RESET}")
        print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
        print(f"{Colors.BLUE}Running checks sequentially...{Colors.RESET}")
        
        check_functions = [
            self.check_homebrew_packages,
            self.check_dependency_packages,
            self.check_language_managers,
            self.check_language_environments,
            self.check_neovim_status,
            self.check_dotfiles_status,
            self.check_system_commands,
            self.check_local_taps,
        ]
        
        results = []
        start_time = time.time()
        
        for check_func in check_functions:
            try:
                result = check_func()
                results.append(result)
                self.print_result(result)
            except Exception as exc:
                error_result = CheckResult(f"[ {Colors.RED}FAIL{Colors.RESET} ] {check_func.__name__}")
                error_result.add_error(f"Check failed with exception: {exc}")
                results.append(error_result)
                self.print_result(error_result)
        
        end_time = time.time()
        
        print(f"\n{Colors.BLUE}All checks completed in {end_time - start_time:.2f} seconds{Colors.RESET}")
        
        # Generate summary
        success = self.generate_summary(results)
        
        return success


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="System Status Checker (Parallel) - Verify cleanup and package status",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run full parallel system check
  %(prog)s --sequential       # Run sequential check (no parallelism)
  %(prog)s --workers 8        # Run with 8 parallel workers
  %(prog)s --packages-only    # Check only package status
  %(prog)s --cleanup-only     # Check only cleanup status
        """
    )
    
    parser.add_argument('--sequential', action='store_true',
                       help='Run checks sequentially instead of in parallel')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers (default: 4)')
    parser.add_argument('--packages-only', action='store_true',
                       help='Check only Homebrew packages')
    parser.add_argument('--cleanup-only', action='store_true',
                       help='Check only cleanup status (no packages)')
    parser.add_argument('--check-type', choices=['cleaned', 'installed'], default='installed',
                       help='Check type: "cleaned" (verify removal) or "installed" (verify installation)')
    
    args = parser.parse_args()
    
    checker = SystemStatusChecker(check_type=args.check_type)
    
    if args.packages_only:
        # Run specific checks sequentially
        results = [
            checker.check_homebrew_packages(),
            checker.check_system_commands()
        ]
        for result in results:
            checker.print_result(result)
        success = checker.generate_summary(results)
    elif args.cleanup_only:
        # Run specific checks sequentially
        results = [
            checker.check_language_managers(),
            checker.check_neovim_status(),
            checker.check_dotfiles_status()
        ]
        for result in results:
            checker.print_result(result)
        success = checker.generate_summary(results)
    else:
        # Run full check
        if args.sequential:
            success = checker.run_sequential_check()
        else:
            success = checker.run_parallel_check(max_workers=args.workers)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()