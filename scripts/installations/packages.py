#!/usr/bin/env python3
"""
Professional Package Manager for Development Environment Setup
Supports selective installation of language-specific toolchains
"""

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


class PackageManager(Enum):
    BREW = "brew"
    BREW_CASK = "brew_cask"
    BREW_TAP = "brew_tap"
    BREW_FORMULA = "brew_formula"  # Custom formula from .rb file
    BREW_LOCAL_TAP = "brew_local_tap"  # Custom formula via local tap
    CURL = "curl"
    SCRIPT = "script"


@dataclass
class Package:
    name: str
    manager: PackageManager
    category: str
    description: str
    install_cmd: Optional[str] = None
    check_cmd: Optional[str] = None
    required: bool = True
    formula_path: Optional[str] = None  # Path to .rb formula file
    tap_name: Optional[str] = None      # Tap name for brew tap
    local_tap_name: Optional[str] = None  # Local tap name (e.g., "local/custom")


class LanguagePackageManager:
    """Professional package manager for development environments"""
    
    def __init__(self):
        self.packages = self._define_packages()
        self.categories = self._get_categories()
    
    def _define_packages(self) -> List[Package]:
        """Define all available packages organized by category"""
        packages = [
            # Core System Tools
            Package("zsh", PackageManager.BREW, "core", "Z shell"),
            Package("git", PackageManager.BREW, "core", "Version control system"),
            Package("tree", PackageManager.BREW, "core", "Directory tree viewer"),
            Package("fzf", PackageManager.BREW, "core", "Fuzzy finder"),
            Package("ripgrep", PackageManager.BREW, "core", "Fast text search (replaces ag)"),
            
            # Editor & Development Tools
            Package("neovim", PackageManager.BREW, "editor", "Modern Vim"),
            Package("universal-ctags", PackageManager.BREW, "editor", "Modern ctags implementation"),
            
            # AI Development Tools
            Package("claude-code", PackageManager.BREW_CASK, "ai-tools", "Claude Code - Terminal-based AI coding assistant"),
            
            # Python Ecosystem - UV Only (replaces pyenv, pip, poetry, pipx)
            Package("uv", PackageManager.BREW, "python", "Complete Python management tool (versions + packages + projects)"),
            
            # Node.js Ecosystem - Modern Stack
            Package("fnm", PackageManager.BREW, "nodejs", "Fast Node.js version manager (faster than nvm)"),
            Package("pnpm", PackageManager.BREW, "nodejs", "Fast, disk space efficient package manager"),
            
            # Go Ecosystem - Minimal & Official
            Package("go", PackageManager.BREW, "golang", "Go programming language"),
            
            # Java Ecosystem Prerequisites - System Level Dependencies
            Package("zip", PackageManager.BREW, "java-prereq", "Archive utility (required for SDKMAN)", required=True),
            Package("unzip", PackageManager.BREW, "java-prereq", "Archive extraction (required for SDKMAN)", required=True),
            Package("curl", PackageManager.BREW, "java-prereq", "Download tool (required for SDKMAN)", required=True),
            
            # Rust Ecosystem
            Package("rustup-init", PackageManager.BREW, "rust", "Rust toolchain installer"),
            
            # DevOps & Infrastructure - Essential Only
            # Package("docker", PackageManager.BREW_CASK, "devops", "Containerization platform"),
            Package("kubectl", PackageManager.BREW, "devops", "Kubernetes CLI"),
            Package("helm", PackageManager.BREW, "devops", "Kubernetes package manager"),
            Package("terraform", PackageManager.BREW_TAP, "devops", "Infrastructure as code", 
                   tap_name="hashicorp/tap", install_cmd="brew install hashicorp/tap/terraform"),
            Package("terragrunt", PackageManager.BREW, "devops", "Terraform wrapper for DRY configurations"),
            
            # Cloud Tools - Major Providers Only
            Package("awscli", PackageManager.BREW, "cloud", "AWS command line interface"),
            Package("gcloud-cli", PackageManager.BREW_CASK, "cloud", "Google Cloud SDK"),
            
            # Network & SSH Tools
            Package("openssh", PackageManager.BREW, "network", "Secure Shell"),
            Package("sshs", PackageManager.BREW, "network", "SSH connection manager"),
            Package("teleport", PackageManager.BREW_LOCAL_TAP, "network", "Modern SSH server for teams", 
                   formula_path="formulas/teleport.rb", local_tap_name="local/custom"),
            
            # Terminal Tools
            Package("tmux", PackageManager.BREW, "terminal", "Terminal multiplexer - essential for development"),
            
            # Fonts
            Package("font-sauce-code-pro-nerd-font", PackageManager.BREW, "fonts", "SauceCodePro Nerd Font for development"),
            
            # System Tools
            Package("xquartz", PackageManager.BREW_CASK, "system", "X11 for macOS"),
            
            # Optional Development Tools
            Package("kind", PackageManager.BREW, "optional", "Kubernetes in Docker", required=False),
            Package("ansible", PackageManager.BREW, "optional", "Configuration management", required=False),
        ]
        
        # Auto-discover custom formulas from formulas/ directory
        packages.extend(self._discover_formula_packages())
        
        return packages
    
    def _discover_formula_packages(self) -> List[Package]:
        """Automatically discover and create packages from formulas/ directory"""
        formula_packages = []
        formulas_dir = Path("formulas")
        
        if not formulas_dir.exists():
            return formula_packages
        
        for formula_file in formulas_dir.glob("*.rb"):
            try:
                # Extract package name from filename (remove .rb extension)
                package_name = formula_file.stem
                
                # Skip teleport as it's manually defined with local tap
                if package_name == "teleport":
                    continue
                
                # Try to extract description from formula file
                description = self._extract_formula_description(formula_file)
                
                # Create package entry
                formula_package = Package(
                    name=package_name,
                    manager=PackageManager.BREW_FORMULA,
                    category="custom",
                    description=description,
                    formula_path=str(formula_file),
                    required=False
                )
                
                formula_packages.append(formula_package)
                
            except Exception as e:
                print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]Warning: Failed to process formula {formula_file}: {e}")
                continue
        
        return formula_packages
    
    def _extract_formula_description(self, formula_file: Path) -> str:
        """Extract description from formula file"""
        try:
            content = formula_file.read_text()
            
            # Look for desc "..." line
            import re
            desc_match = re.search(r'desc\s+"([^"]+)"', content)
            if desc_match:
                return desc_match.group(1)
            
            # Fallback to generic description
            return f"Custom formula: {formula_file.stem}"
            
        except Exception:
            return f"Custom formula: {formula_file.stem}"
    
    def _get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(pkg.category for pkg in self.packages))
    
    def _run_command(self, cmd: str, description: str = "") -> bool:
        """Execute a command and return success status"""
        print(f"🔄 {description or cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  capture_output=True, text=True)
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] {description or cmd}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Failed: {description or cmd}")
            print(f"   Error: {e.stderr.strip()}")
            return False
    
    def _check_package_installed(self, package: Package) -> bool:
        """Check if a package is already installed"""
        if package.check_cmd:
            try:
                subprocess.run(package.check_cmd, shell=True, check=True, 
                             capture_output=True)
                return True
            except subprocess.CalledProcessError:
                return False
        
        # Default check based on package manager
        if package.manager in [PackageManager.BREW, PackageManager.BREW_TAP, PackageManager.BREW_FORMULA]:
            cmd = f"brew list {package.name}"
        elif package.manager == PackageManager.BREW_LOCAL_TAP:
            # For local tap packages, check if installed from the tap
            cmd = f"brew list {package.name}"
        elif package.manager == PackageManager.BREW_CASK:
            cmd = f"brew list --cask {package.name}"
        else:
            return False
        
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _install_tap_if_needed(self, tap_name: str) -> bool:
        """Install brew tap if not already added"""
        try:
            # Check if tap is already added
            result = subprocess.run("brew tap", shell=True, check=True, 
                                  capture_output=True, text=True)
            if tap_name in result.stdout:
                return True
            
            # Add the tap
            return self._run_command(f"brew tap {tap_name}", f"Adding tap {tap_name}")
        except subprocess.CalledProcessError:
            return self._run_command(f"brew tap {tap_name}", f"Adding tap {tap_name}")
    
    def _ensure_local_tap(self, tap_name: str) -> bool:
        """Ensure local tap exists, create if needed"""
        try:
            # Check if tap already exists
            result = subprocess.run("brew tap", shell=True, check=True, 
                                  capture_output=True, text=True)
            if tap_name in result.stdout:
                return True
            
            # Create the local tap
            return self._run_command(f"brew tap-new {tap_name}", f"Creating local tap {tap_name}")
        except subprocess.CalledProcessError:
            return self._run_command(f"brew tap-new {tap_name}", f"Creating local tap {tap_name}")
    
    def _copy_formula_to_local_tap(self, package: Package) -> bool:
        """Copy formula file to local tap directory"""
        if not package.formula_path or not package.local_tap_name:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Missing formula path or local tap name for {package.name}")
            return False
        
        formula_path = Path(package.formula_path)
        if not formula_path.exists():
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula file not found: {formula_path}")
            return False
        
        try:
            # Get tap repository path
            result = subprocess.run(f"brew --repo {package.local_tap_name}", 
                                  shell=True, check=True, capture_output=True, text=True)
            tap_repo_path = Path(result.stdout.strip())
            
            # Ensure Formula directory exists
            formula_dir = tap_repo_path / "Formula"
            formula_dir.mkdir(exist_ok=True)
            
            # Copy formula file
            target_path = formula_dir / formula_path.name
            import shutil
            shutil.copy2(formula_path, target_path)
            
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Copied {formula_path.name} to {package.local_tap_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Failed to copy formula to local tap: {e}")
            return False
        except Exception as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Error copying formula: {e}")
            return False
    
    def _install_from_local_tap(self, package: Package) -> bool:
        """Install package from local tap"""
        if not package.local_tap_name:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] No local tap name specified for {package.name}")
            return False
        
        # Ensure local tap exists
        if not self._ensure_local_tap(package.local_tap_name):
            return False
        
        # Copy formula to local tap
        if not self._copy_formula_to_local_tap(package):
            return False
        
        # Install from local tap
        cmd = f"brew install {package.local_tap_name}/{package.name}"
        return self._run_command(cmd, f"Installing {package.name} from local tap")
    
    def _install_from_formula(self, package: Package) -> bool:
        """Install package from custom .rb formula file"""
        if not package.formula_path:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] No formula path specified for {package.name}")
            return False
        
        formula_full_path = os.path.abspath(package.formula_path)
        if not os.path.exists(formula_full_path):
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula file not found: {formula_full_path}")
            return False
        
        cmd = f"brew install {formula_full_path}"
        return self._run_command(cmd, f"Installing {package.name} from formula")
    
    def _install_package(self, package: Package) -> bool:
        """Install a single package"""
        if self._check_package_installed(package):
            print(f"⏭️  {package.name} already installed")
            return True
        
        # Handle custom install command
        if package.install_cmd:
            return self._run_command(package.install_cmd, f"Installing {package.name}")
        
        # Handle different package managers
        if package.manager == PackageManager.BREW:
            cmd = f"brew install {package.name}"
        elif package.manager == PackageManager.BREW_CASK:
            cmd = f"brew install --cask {package.name}"
        elif package.manager == PackageManager.BREW_TAP:
            # Install tap first if needed
            if package.tap_name and not self._install_tap_if_needed(package.tap_name):
                return False
            cmd = f"brew install {package.name}"
        elif package.manager == PackageManager.BREW_FORMULA:
            return self._install_from_formula(package)
        elif package.manager == PackageManager.BREW_LOCAL_TAP:
            return self._install_from_local_tap(package)
        else:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Unknown package manager for {package.name}")
            return False
        
        return self._run_command(cmd, f"Installing {package.name}")
    
    def _ensure_homebrew(self) -> bool:
        """Ensure Homebrew is installed"""
        try:
            subprocess.run("brew --version", shell=True, check=True, 
                         capture_output=True)
            return True
        except subprocess.CalledProcessError:
            print("🔄 Installing Homebrew...")
            cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            return self._run_command(cmd, "Installing Homebrew")
    
    def install_category(self, category: str, skip_optional: bool = True) -> bool:
        """Install all packages in a specific category"""
        if category not in self.categories:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Unknown category: {category}")
            print(f"Available categories: {', '.join(self.categories)}")
            return False
        
        packages = [pkg for pkg in self.packages if pkg.category == category]
        if skip_optional:
            packages = [pkg for pkg in packages if pkg.required]
        
        print(f"\n📦 Installing {category} packages...")
        print(f"Packages: {', '.join(pkg.name for pkg in packages)}")
        
        success_count = 0
        for package in packages:
            if self._install_package(package):
                success_count += 1
        
        print(f"\n[ {Colors.GREEN}OK{Colors.RESET} ] {success_count}/{len(packages)} packages installed successfully")
        return success_count == len(packages)
    
    def _get_obsolete_packages(self) -> List[str]:
        """Get list of packages that should be removed (replaced by modern alternatives)"""
        obsolete_packages = [
            # Python ecosystem - replaced by uv
            "pyenv",
            "python@3.12", 
            "python@3.13",
            "pipx",
            
            # Node.js ecosystem - replaced by fnm
            "nvm",
            
            # Search tools - replaced by ripgrep
            "the_silver_searcher",  # ag command
            
            # Duplicate cloud tools
            "gcloud-cli",  # duplicate of google-cloud-sdk
        ]
        return obsolete_packages
    
    def _cleanup_obsolete_packages(self) -> bool:
        """Remove obsolete packages that have been replaced by modern alternatives"""
        obsolete_packages = self._get_obsolete_packages()
        
        print("🧹 Checking for obsolete packages to clean up...")
        
        # Get list of installed packages
        try:
            result = subprocess.run("brew list --formula", shell=True, check=True, 
                                  capture_output=True, text=True)
            installed_formulae = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            result = subprocess.run("brew list --cask", shell=True, check=True, 
                                  capture_output=True, text=True)
            installed_casks = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            installed_packages = installed_formulae + installed_casks
            
        except subprocess.CalledProcessError:
            print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ] Could not get list of installed packages")
            return True  # Continue anyway
        
        # Find obsolete packages that are actually installed
        to_remove = [pkg for pkg in obsolete_packages if pkg in installed_packages]
        
        if not to_remove:
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] No obsolete packages found")
            return True
        
        print(f"📦 Found {len(to_remove)} obsolete packages to remove:")
        for pkg in to_remove:
            print(f"  • {pkg}")
        
        # Ask for confirmation
        print("\n🤔 These packages have modern replacements:")
        print("  • pyenv, python@3.x, pipx → uv (complete Python management)")
        print("  • nvm → fnm (faster Node.js version manager)")
        print("  • the_silver_searcher → ripgrep (faster text search)")
        print("  • gcloud-cli → google-cloud-sdk (avoid duplicates)")
        
        response = input("\n❓ Remove obsolete packages? [y/N]: ").lower().strip()
        if response not in ['y', 'yes']:
            print("⏭️  Skipping cleanup")
            return True
        
        # Remove obsolete packages
        success_count = 0
        for pkg in to_remove:
            # Try normal uninstall first
            if self._run_command(f"brew uninstall {pkg}", f"Removing obsolete package: {pkg}"):
                success_count += 1
            else:
                # If failed due to dependencies, try with --ignore-dependencies
                print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]{pkg} has dependencies, trying force removal...")
                if self._run_command(f"brew uninstall --ignore-dependencies {pkg}", 
                                   f"Force removing obsolete package: {pkg}"):
                    success_count += 1
        
        print(f"\n[ {Colors.GREEN}OK{Colors.RESET} ] Removed {success_count}/{len(to_remove)} obsolete packages")
        return success_count == len(to_remove)
    
    def install_all(self, skip_optional: bool = True, cleanup_obsolete: bool = True) -> bool:
        """Install all packages"""
        if not self._ensure_homebrew():
            return False
        
        # Update Homebrew
        self._run_command("brew update", "Updating Homebrew")
        
        # Cleanup obsolete packages first
        if cleanup_obsolete:
            self._cleanup_obsolete_packages()
        
        # Install by category in order
        install_order = ["core", "editor", "ai-tools", "terminal", "python", "nodejs", "golang", "java-prereq", 
                        "rust", "devops", "cloud", "network", "fonts", "system", "custom"]
        
        if not skip_optional:
            install_order.append("optional")
        
        all_success = True
        for category in install_order:
            if category in self.categories:
                success = self.install_category(category, skip_optional)
                all_success = all_success and success
        
        return all_success
    
    def list_packages(self, category: Optional[str] = None) -> None:
        """List available packages"""
        packages = self.packages
        if category:
            packages = [pkg for pkg in packages if pkg.category == category]
        
        # Group by category
        by_category = {}
        for pkg in packages:
            if pkg.category not in by_category:
                by_category[pkg.category] = []
            by_category[pkg.category].append(pkg)
        
        for cat, pkgs in sorted(by_category.items()):
            print(f"\n📂 {cat.upper()}")
            for pkg in sorted(pkgs, key=lambda x: x.name):
                status = "required" if pkg.required else "optional"
                print(f"  • {pkg.name:<20} - {pkg.description} ({status})")
    
    def install_all_formulas(self) -> bool:
        """Install all custom formulas found in formulas/ directory"""
        formula_packages = self._discover_formula_packages()
        
        if not formula_packages:
            print("📂 No custom formulas found in formulas/ directory")
            return True
        
        print(f"\n📦 Installing {len(formula_packages)} custom formulas...")
        print(f"Formulas: {', '.join(pkg.name for pkg in formula_packages)}")
        
        success_count = 0
        for package in formula_packages:
            if self._install_package(package):
                success_count += 1
        
        print(f"\n[ {Colors.GREEN}OK{Colors.RESET} ] {success_count}/{len(formula_packages)} custom formulas installed successfully")
        return success_count == len(formula_packages)
    
    def list_discovered_formulas(self) -> None:
        """List all discovered formulas from formulas/ directory"""
        formula_packages = self._discover_formula_packages()
        
        if not formula_packages:
            print("📂 No custom formulas found in formulas/ directory")
            print("   Add .rb files to the formulas/ directory to auto-discover them")
            return
        
        print(f"📂 DISCOVERED FORMULAS ({len(formula_packages)} found)")
        for pkg in sorted(formula_packages, key=lambda x: x.name):
            status = "[ {Colors.GREEN}OK{Colors.RESET} ]" if self._check_package_installed(pkg) else "[ {Colors.RED}FAIL{Colors.RESET} ]"
            print(f"  {status} {pkg.name:<20} - {pkg.description}")
            print(f"      Formula: {pkg.formula_path}")
        print()
        print("💡 Use 'make packages-formulas' to install all discovered formulas")
    
    def status(self) -> None:
        """Show installation status of all packages"""
        print("📊 Package Installation Status\n")
        
        by_category = {}
        for pkg in self.packages:
            if pkg.category not in by_category:
                by_category[pkg.category] = []
            by_category[pkg.category].append(pkg)
        
        for category, packages in sorted(by_category.items()):
            print(f"📂 {category.upper()}")
            for pkg in sorted(packages, key=lambda x: x.name):
                installed = self._check_package_installed(pkg)
                status_icon = "[ {Colors.GREEN}OK{Colors.RESET} ]" if installed else "[ {Colors.RED}FAIL{Colors.RESET} ]"
                print(f"  {status_icon} {pkg.name:<20} - {pkg.description}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Professional Development Environment Package Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s install --all                    # Install all required packages
  %(prog)s install --category python       # Install Python ecosystem
  %(prog)s install --category golang       # Install Go ecosystem
  %(prog)s install-formulas                # Install all discovered custom formulas
  %(prog)s list                            # List all packages
  %(prog)s list --category python          # List Python packages
  %(prog)s list-formulas                   # List all discovered custom formulas
  %(prog)s status                          # Show installation status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install packages')
    install_group = install_parser.add_mutually_exclusive_group(required=True)
    install_group.add_argument('--all', action='store_true', 
                              help='Install all required packages')
    install_group.add_argument('--category', type=str, 
                              help='Install packages from specific category')
    install_parser.add_argument('--include-optional', action='store_true',
                               help='Include optional packages')
    install_parser.add_argument('--no-cleanup', action='store_true',
                               help='Skip cleanup of obsolete packages')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available packages')
    list_parser.add_argument('--category', type=str, 
                            help='List packages from specific category')
    
    # Install formulas command
    subparsers.add_parser('install-formulas', help='Install all discovered custom formulas')
    
    # List formulas command  
    subparsers.add_parser('list-formulas', help='List all discovered custom formulas')
    
    # Cleanup command
    subparsers.add_parser('cleanup', help='Remove obsolete packages with modern replacements')
    
    # Status command
    subparsers.add_parser('status', help='Show installation status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = LanguagePackageManager()
    
    if args.command == 'install':
        skip_optional = not args.include_optional
        
        if args.all:
            skip_optional = not args.include_optional
            cleanup_obsolete = not args.no_cleanup
            success = manager.install_all(skip_optional, cleanup_obsolete)
            sys.exit(0 if success else 1)
        elif args.category:
            success = manager.install_category(args.category, skip_optional)
            sys.exit(0 if success else 1)
    
    elif args.command == 'install-formulas':
        success = manager.install_all_formulas()
        sys.exit(0 if success else 1)
    
    elif args.command == 'list-formulas':
        manager.list_discovered_formulas()
    
    elif args.command == 'cleanup':
        success = manager._cleanup_obsolete_packages()
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        manager.list_packages(args.category)
    
    elif args.command == 'status':
        manager.status()


if __name__ == '__main__':
    main()