#!/usr/bin/env python3
"""
Language Version Managers Setup Script
Installs and configures modern language version managers for development.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


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


def info(message: str) -> None:
    print(f"  [ {Colors.BLUE}..{Colors.RESET} ] {message}")


def success(message: str) -> None:
    print(f"  [ {Colors.GREEN}OK{Colors.RESET} ] {message}")


def warning(message: str) -> None:
    print(f"  [ {Colors.YELLOW}WARN{Colors.RESET} ]{message}")


def fail(message: str) -> None:
    print(f"  [ {Colors.RED}FAIL{Colors.RESET} ] {message}")
    sys.exit(1)


def run_command(cmd: List[str], capture_output: bool = True, check: bool = False, shell: bool = False) -> Optional[subprocess.CompletedProcess]:
    """Run a command and return the result."""
    try:
        if shell:
            cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
            result = subprocess.run(cmd_str, capture_output=capture_output, text=True, check=check, shell=True)
        else:
            result = subprocess.run(cmd, capture_output=capture_output, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        if not capture_output:
            warning(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        return None
    except FileNotFoundError:
        return None


def command_exists(command: str) -> bool:
    """Check if a command exists in PATH."""
    result = run_command(['which', command])
    return result is not None and result.returncode == 0


def setup_sdkman_java() -> None:
    """Setup SDKMAN for Java management."""
    info("Setting up SDKMAN for Java management...")
    
    home = Path.home()
    sdkman_dir = home / ".sdkman"
    
    # Check system prerequisites
    info("Checking system prerequisites for SDKMAN...")
    required_tools = ['zip', 'unzip', 'curl', 'sed']
    
    for tool in required_tools:
        if not command_exists(tool):
            fail(f"{tool} is required but not installed. Run 'make packages-java-prereq' first.")
    
    success("System prerequisites verified")
    
    # Install SDKMAN if not present
    if not sdkman_dir.exists():
        info("Installing SDKMAN core manager...")
        
        # Download and install SDKMAN
        install_cmd = 'curl -s "https://get.sdkman.io" | bash'
        result = run_command(install_cmd, capture_output=False, shell=True)
        
        if sdkman_dir.exists():
            success("SDKMAN core manager installed at ~/.sdkman")
        else:
            fail("SDKMAN installation failed")
    else:
        success("SDKMAN core manager already installed")
    
    # Source SDKMAN for use in this script
    sdkman_init = sdkman_dir / "bin" / "sdkman-init.sh"
    if not sdkman_init.exists():
        fail("SDKMAN initialization script not found")
    
    # Install Java ecosystem packages
    info("Installing Java ecosystem packages via SDKMAN...")
    
    # Define SDKMAN commands
    sdk_commands = [
        # Install Eclipse Temurin JDK 21 (LTS) as default
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install java 21.0.1-tem --default',
        # Install Eclipse Temurin JDK 17 (Previous LTS)
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install java 17.0.9-tem',
        # Install Maven
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install maven',
        # Install Gradle
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install gradle',
    ]
    
    descriptions = [
        "Eclipse Temurin JDK 21 (LTS) as default",
        "Eclipse Temurin JDK 17 (Previous LTS)",
        "Maven build tool",
        "Gradle build automation"
    ]
    
    for cmd, desc in zip(sdk_commands, descriptions):
        info(f"Installing {desc}...")
        result = run_command(cmd, capture_output=False, shell=True)
        if result is None or result.returncode != 0:
            # Check if already installed
            check_cmd = f'source ~/.sdkman/bin/sdkman-init.sh && sdk current {desc.split()[0].lower()}'
            check_result = run_command(check_cmd, shell=True)
            if check_result and check_result.returncode == 0:
                success(f"{desc} already installed")
            else:
                warning(f"Failed to install {desc}, but continuing...")
        else:
            success(f"{desc} installed")
    
    success("Java ecosystem setup complete via SDKMAN")


def setup_rust() -> None:
    """Initialize Rust toolchain."""
    info("Initializing Rust toolchain...")
    
    home = Path.home()
    cargo_dir = home / ".cargo"
    
    if command_exists('rustup-init'):
        if not cargo_dir.exists():
            info("Installing Rust toolchain...")
            result = run_command(['rustup-init', '-y', '--no-modify-path'], capture_output=False)
            if result and result.returncode == 0:
                success("Rust toolchain initialized")
            else:
                warning("Rust installation may have failed")
        else:
            success("Rust toolchain already initialized")
    else:
        info("rustup-init not found, Rust will be available after package installation")


def setup_python_uv() -> None:
    """Setup Python with uv (modern Python version and package manager)."""
    info("Setting up Python with uv...")
    
    if command_exists('uv'):
        # Install latest Python version
        info("Installing Python 3.12 via uv...")
        result = run_command(['uv', 'python', 'install', '3.12'], capture_output=False)
        if result and result.returncode == 0:
            success("Python 3.12 installed via uv")
        else:
            warning("Python 3.12 may already be installed")
        
        # Set as default
        info("Setting Python 3.12 as default...")
        result = run_command(['uv', 'python', 'pin', '3.12'], capture_output=False)
        if result and result.returncode == 0:
            success("Python 3.12 set as default")
        else:
            warning("Failed to set Python 3.12 as default")
    else:
        info("uv not found, will be available after package installation")


def setup_nodejs_fnm() -> None:
    """Setup Node.js with fnm (fast Node version manager)."""
    info("Setting up Node.js with fnm...")
    
    if command_exists('fnm'):
        # Install LTS Node.js
        info("Installing Node.js LTS via fnm...")
        result = run_command(['fnm', 'install', '--lts'], capture_output=False)
        if result and result.returncode == 0:
            success("Node.js LTS installed via fnm")
        else:
            warning("Node.js LTS may already be installed")
        
        # Set as default
        info("Setting Node.js LTS as default...")
        result = run_command(['fnm', 'default', 'lts-latest'], capture_output=False)
        if result and result.returncode == 0:
            success("Node.js LTS set as default")
        else:
            warning("Failed to set Node.js LTS as default")
    else:
        info("fnm not found, will be available after package installation")


def show_setup_info() -> None:
    """Show setup information and next steps."""
    print(f"\n{Colors.GREEN}# Language Version Managers Setup Complete!{Colors.RESET}\n")
    
    print("Installed version managers:")
    print("  📦 Python: uv (complete Python version + package management)")
    print("  📦 Node.js: fnm (fast Node version manager)")
    print("  📦 Go: Built-in version management")
    print("  📦 Java: SDKMAN (comprehensive Java ecosystem with total isolation)")
    print("  📦 Rust: rustup (official Rust toolchain)")
    print()
    
    print("Next steps - Use language versions:")
    print()
    print("  # Python (uv handles everything - no pyenv needed)")
    print("  uv python install 3.11")
    print("  uv python pin 3.11")
    print("  uv python list                    # List installed versions")
    print("  uv venv                           # Create virtual environment")
    print("  uv pip install package           # Install packages")
    print()
    
    print("  # Node.js (fnm is faster than nvm)")
    print("  fnm install 18")
    print("  fnm use 18")
    print("  fnm default 18")
    print("  fnm list                          # List installed versions")
    print()
    
    print("  # Go (use official installer or brew)")
    print("  go version                        # Check version")
    print("  go mod init project               # Initialize module")
    print()
    
    print("  # Java (SDKMAN provides total isolation and easy switching)")
    print("  source ~/.sdkman/bin/sdkman-init.sh")
    print("  sdk list java                     # See all available JDKs")
    print("  sdk use java 21.0.1-tem         # Switch to Java 21")
    print("  sdk use java 17.0.9-tem         # Switch to Java 17")
    print("  sdk default java 21.0.1-tem     # Set permanent default")
    print()
    print("  # Installed Java ecosystem at ~/.sdkman/candidates/:")
    print("  #   java/21.0.1-tem/    (Eclipse Temurin JDK 21 LTS)")
    print("  #   java/17.0.9-tem/    (Eclipse Temurin JDK 17 LTS)")
    print("  #   maven/latest/       (Java build tool)")
    print("  #   gradle/latest/      (Modern build automation)")
    print()
    
    print("  # Rust")
    print("  source ~/.cargo/env")
    print("  rustup update stable")
    print("  cargo --version                   # Check version")
    print("  cargo new project                 # Create new project")
    print()


def main():
    """Main setup function."""
    print(f"\n{Colors.BLUE}##########################################{Colors.RESET}")
    print(f"{Colors.BLUE}# Language Version Managers Setup       #{Colors.RESET}")
    print(f"{Colors.BLUE}##########################################{Colors.RESET}\n")
    
    # Setup each language manager
    setup_sdkman_java()
    setup_rust()
    setup_python_uv()
    setup_nodejs_fnm()
    
    show_setup_info()


if __name__ == "__main__":
    main()