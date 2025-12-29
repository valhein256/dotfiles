#!/usr/bin/env python3
"""
Advanced Brew Installation Flow Manager
Supports direct brew install and external .rb formula files
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class BrewManager:
    """Advanced Brew package manager with formula support"""
    
    def __init__(self):
        self.formulas_dir = Path("formulas")
        self.ensure_formulas_dir()
    
    def ensure_formulas_dir(self):
        """Ensure formulas directory exists"""
        self.formulas_dir.mkdir(exist_ok=True)
    
    def _run_command(self, cmd: str, description: str = "") -> bool:
        """Execute a command and return success status"""
        print(f"🔄 {description or cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  capture_output=True, text=True)
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] {description or cmd}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Failed: {description or cmd}")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            return False
    
    def ensure_homebrew(self) -> bool:
        """Ensure Homebrew is installed"""
        try:
            subprocess.run("brew --version", shell=True, check=True, 
                         capture_output=True)
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Homebrew is already installed")
            return True
        except subprocess.CalledProcessError:
            print("🔄 Installing Homebrew...")
            cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            return self._run_command(cmd, "Installing Homebrew")
    
    def ensure_local_tap(self, tap_name: str = "local/custom") -> bool:
        """Ensure local tap exists, create if needed"""
        try:
            # Check if tap already exists
            result = subprocess.run("brew tap", shell=True, check=True, 
                                  capture_output=True, text=True)
            if tap_name in result.stdout:
                print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Local tap {tap_name} already exists")
                return True
            
            # Create the local tap
            return self._run_command(f"brew tap-new {tap_name}", f"Creating local tap {tap_name}")
        except subprocess.CalledProcessError:
            return self._run_command(f"brew tap-new {tap_name}", f"Creating local tap {tap_name}")
    
    def install_formula_via_local_tap(self, formula_path: str, tap_name: str = "local/custom") -> bool:
        """Install formula via local tap (recommended method)"""
        if not self.ensure_homebrew():
            return False
        
        formula_file = Path(formula_path)
        if not formula_file.exists():
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula file not found: {formula_path}")
            return False
        
        # Ensure local tap exists
        if not self.ensure_local_tap(tap_name):
            return False
        
        try:
            # Get tap repository path
            result = subprocess.run(f"brew --repo {tap_name}", 
                                  shell=True, check=True, capture_output=True, text=True)
            tap_repo_path = Path(result.stdout.strip())
            
            # Ensure Formula directory exists
            formula_dir = tap_repo_path / "Formula"
            formula_dir.mkdir(exist_ok=True)
            
            # Copy formula file
            target_path = formula_dir / formula_file.name
            import shutil
            shutil.copy2(formula_file, target_path)
            
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Copied {formula_file.name} to {tap_name}")
            
            # Extract package name from formula file
            package_name = formula_file.stem
            
            # Install from local tap
            cmd = f"brew install {tap_name}/{package_name}"
            return self._run_command(cmd, f"Installing {package_name} from local tap")
            
        except subprocess.CalledProcessError as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Failed to install via local tap: {e}")
            return False
        except Exception as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Error: {e}")
            return False
            cmd = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            return self._run_command(cmd, "Installing Homebrew")
    
    def install_package(self, package_name: str, cask: bool = False) -> bool:
        """Install a package using standard brew install"""
        if not self.ensure_homebrew():
            return False
        
        install_type = "--cask" if cask else ""
        cmd = f"brew install {install_type} {package_name}".strip()
        return self._run_command(cmd, f"Installing {package_name}")
    
    def install_from_formula(self, formula_path: str) -> bool:
        """Install a package from a .rb formula file"""
        if not self.ensure_homebrew():
            return False
        
        formula_file = Path(formula_path)
        if not formula_file.exists():
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula file not found: {formula_path}")
            return False
        
        if not formula_file.suffix == '.rb':
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Invalid formula file extension: {formula_path}")
            return False
        
        absolute_path = formula_file.resolve()
        cmd = f"brew install {absolute_path}"
        return self._run_command(cmd, f"Installing from formula: {formula_file.name}")
    
    def install_from_tap(self, tap_name: str, package_name: str) -> bool:
        """Install a package from a specific tap"""
        if not self.ensure_homebrew():
            return False
        
        # Add tap if not already added
        if not self._add_tap(tap_name):
            return False
        
        cmd = f"brew install {tap_name}/{package_name}"
        return self._run_command(cmd, f"Installing {package_name} from {tap_name}")
    
    def _add_tap(self, tap_name: str) -> bool:
        """Add a brew tap if not already added"""
        try:
            # Check if tap is already added
            result = subprocess.run("brew tap", shell=True, check=True, 
                                  capture_output=True, text=True)
            if tap_name in result.stdout:
                print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Tap {tap_name} already added")
                return True
        except subprocess.CalledProcessError:
            pass
        
        return self._run_command(f"brew tap {tap_name}", f"Adding tap {tap_name}")
    
    def list_formulas(self) -> List[Path]:
        """List available custom formula files"""
        return list(self.formulas_dir.glob("*.rb"))
    
    def create_formula_template(self, name: str) -> bool:
        """Create a template formula file"""
        formula_file = self.formulas_dir / f"{name}.rb"
        
        if formula_file.exists():
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula {name}.rb already exists")
            return False
        
        class_name = ''.join(word.capitalize() for word in name.split('-'))
        
        template = f'''class {class_name} < Formula
  desc "Description of {name}"
  homepage "https://github.com/example/{name}"
  url "https://github.com/example/{name}/archive/v1.0.0.tar.gz"
  sha256 "your_sha256_hash_here"
  license "MIT"

  depends_on "go" => :build  # Adjust dependencies as needed

  def install
    # Build and install commands
    system "make", "install", "PREFIX=#{prefix}"
  end

  test do
    system "#{bin}/{name}", "--version"
  end
end'''
        
        try:
            formula_file.write_text(template)
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Created formula template: {formula_file}")
            print(f"   Edit {formula_file} to customize the formula")
            return True
        except Exception as e:
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Failed to create formula: {e}")
            return False
    
    def validate_formula(self, formula_path: str) -> bool:
        """Validate a formula file syntax"""
        formula_file = Path(formula_path)
        if not formula_file.exists():
            print(f"[ {Colors.RED}FAIL{Colors.RESET} ] Formula file not found: {formula_path}")
            return False
        
        cmd = f"brew install --dry-run {formula_file.resolve()}"
        return self._run_command(cmd, f"Validating formula: {formula_file.name}")
    
    def uninstall_package(self, package_name: str) -> bool:
        """Uninstall a package"""
        cmd = f"brew uninstall {package_name}"
        return self._run_command(cmd, f"Uninstalling {package_name}")
    
    def update_brew(self) -> bool:
        """Update Homebrew and all packages"""
        if not self.ensure_homebrew():
            return False
        
        success = True
        success &= self._run_command("brew update", "Updating Homebrew")
        success &= self._run_command("brew upgrade", "Upgrading packages")
        return success


def main():
    parser = argparse.ArgumentParser(
        description="Advanced Brew Installation Flow Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s install git                          # Standard brew install
  %(prog)s install --cask docker                # Install cask package
  %(prog)s install-formula formulas/lazygit.rb  # Install from .rb file
  %(prog)s install-tap hashicorp/tap terraform  # Install from tap
  %(prog)s create-template my-tool              # Create formula template
  %(prog)s list-formulas                        # List available formulas
  %(prog)s validate formulas/lazygit.rb         # Validate formula
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install package')
    install_parser.add_argument('package', help='Package name to install')
    install_parser.add_argument('--cask', action='store_true', help='Install as cask')
    
    # Install from formula
    formula_parser = subparsers.add_parser('install-formula', help='Install from .rb formula file')
    formula_parser.add_argument('formula_path', help='Path to .rb formula file')
    
    # Install from tap
    tap_parser = subparsers.add_parser('install-tap', help='Install from specific tap')
    tap_parser.add_argument('tap_name', help='Tap name (e.g., hashicorp/tap)')
    tap_parser.add_argument('package', help='Package name')
    
    # Install from local tap (recommended for custom formulas)
    local_tap_parser = subparsers.add_parser('install-local-tap', help='Install formula via local tap (recommended)')
    local_tap_parser.add_argument('formula_path', help='Path to .rb formula file')
    local_tap_parser.add_argument('--tap-name', default='local/custom', help='Local tap name (default: local/custom)')
    
    # Create template
    template_parser = subparsers.add_parser('create-template', help='Create formula template')
    template_parser.add_argument('name', help='Formula name')
    
    # List formulas
    subparsers.add_parser('list-formulas', help='List available custom formulas')
    
    # Validate formula
    validate_parser = subparsers.add_parser('validate', help='Validate formula syntax')
    validate_parser.add_argument('formula_path', help='Path to .rb formula file')
    
    # Uninstall
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall package')
    uninstall_parser.add_argument('package', help='Package name to uninstall')
    
    # Update
    subparsers.add_parser('update', help='Update Homebrew and packages')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = BrewManager()
    
    if args.command == 'install':
        success = manager.install_package(args.package, args.cask)
        sys.exit(0 if success else 1)
    
    elif args.command == 'install-formula':
        success = manager.install_from_formula(args.formula_path)
        sys.exit(0 if success else 1)
    
    elif args.command == 'install-tap':
        success = manager.install_from_tap(args.tap_name, args.package)
        sys.exit(0 if success else 1)
    
    elif args.command == 'install-local-tap':
        success = manager.install_formula_via_local_tap(args.formula_path, args.tap_name)
        sys.exit(0 if success else 1)
    
    elif args.command == 'create-template':
        success = manager.create_formula_template(args.name)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list-formulas':
        formulas = manager.list_formulas()
        if formulas:
            print("📂 Available custom formulas:")
            for formula in formulas:
                print(f"  • {formula.name}")
        else:
            print("📂 No custom formulas found in formulas/ directory")
    
    elif args.command == 'validate':
        success = manager.validate_formula(args.formula_path)
        sys.exit(0 if success else 1)
    
    elif args.command == 'uninstall':
        success = manager.uninstall_package(args.package)
        sys.exit(0 if success else 1)
    
    elif args.command == 'update':
        success = manager.update_brew()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()