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


def _find_modern_bash() -> Optional[str]:
    """Find a Bash 4+ binary. macOS ships /bin/bash 3.2 forever (GPLv3 licensing)
    and SDKMAN's installer hard-requires Bash 4+."""
    for path in ('/opt/homebrew/bin/bash', '/usr/local/bin/bash'):
        if Path(path).exists():
            return path
    return None


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

    modern_bash = _find_modern_bash()
    if not modern_bash:
        fail("Bash 4+ not found. Run 'brew install bash' first — "
             "macOS ships /bin/bash 3.2 and SDKMAN's installer rejects it.")

    # Install SDKMAN if not present
    if not sdkman_dir.exists():
        info(f"Installing SDKMAN core manager (using {modern_bash})...")

        # Pipe the installer to Homebrew bash explicitly; piping to /bin/bash (3.2) fails the version check.
        install_cmd = f'curl -s "https://get.sdkman.io" | {modern_bash}'
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

    # Default to Amazon Corretto 17 to match the EAIS-Parser Dockerfile
    # (FROM amazoncorretto:17). Temurin 21 stays available as a secondary toolchain.
    sdk_commands = [
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install java 17.0.13-amzn',
        'source ~/.sdkman/bin/sdkman-init.sh && sdk default java 17.0.13-amzn',
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install java 21.0.5-tem',
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install maven',
        'source ~/.sdkman/bin/sdkman-init.sh && sdk install gradle',
    ]

    descriptions = [
        "Amazon Corretto JDK 17 (matches project Dockerfile)",
        "Set Corretto 17 as the default JDK",
        "Eclipse Temurin JDK 21 (LTS, secondary)",
        "Maven build tool",
        "Gradle build automation"
    ]
    
    # SDKMAN's sdk function uses Bash 4+ syntax (e.g. ${var^^}); macOS /bin/sh is bash 3.2.
    # Run every sdk command through Homebrew bash explicitly.
    def _bash(cmd: str) -> Optional[subprocess.CompletedProcess]:
        return run_command([modern_bash, '-c', cmd], capture_output=False)

    def _bash_capture(cmd: str) -> Optional[subprocess.CompletedProcess]:
        return run_command([modern_bash, '-c', cmd])

    for cmd, desc in zip(sdk_commands, descriptions):
        info(f"Installing {desc}...")
        result = _bash(cmd)
        if result is None or result.returncode != 0:
            # Check if already installed
            check_cmd = f'source ~/.sdkman/bin/sdkman-init.sh && sdk current {desc.split()[0].lower()}'
            check_result = _bash_capture(check_cmd)
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
    
    def _install_python(version: str) -> None:
        info(f"Installing Python {version} via uv...")
        result = run_command(['uv', 'python', 'install', version], capture_output=False)
        if result and result.returncode == 0:
            success(f"Python {version} installed via uv")
            return
        # `uv python install` fails when the version is missing AND can't be
        # downloaded (e.g. TLS / network errors). Distinguish "already present"
        # from a real failure by probing the installed list.
        check = run_command(['uv', 'python', 'find', version])
        if check and check.returncode == 0 and check.stdout.strip():
            success(f"Python {version} already installed")
        else:
            warning(f"Failed to install Python {version} (not present)")

    if command_exists('uv'):
        _install_python('3.12')
        _install_python('3.11')
        
        # Set Python 3.12 as default
        info("Setting Python 3.12 as default...")
        result = run_command(['uv', 'python', 'pin', '3.12'], capture_output=False)
        if result and result.returncode == 0:
            success("Python 3.12 set as default")
        else:
            warning("Failed to set Python 3.12 as default")
        
        # Install common global tools
        info("Installing common Python tools globally...")
        global_tools = ['black', 'ruff', 'pytest', 'mypy', 'ipython']
        installed = run_command(['uv', 'tool', 'list'])
        installed_names = set()
        if installed and installed.returncode == 0 and installed.stdout:
            # `uv tool list` prints "<name> v<version>" then indented "- <bin>" lines.
            for line in installed.stdout.splitlines():
                if line and not line.startswith(' ') and not line.startswith('-'):
                    installed_names.add(line.split()[0])
        for tool in global_tools:
            if tool in installed_names:
                success(f"{tool} already installed")
                continue
            result = run_command(['uv', 'tool', 'install', tool], capture_output=True)
            if result and result.returncode == 0:
                success(f"Installed {tool} globally")
            else:
                err = (result.stderr.strip() if result and result.stderr else "unknown error")
                warning(f"Failed to install {tool} globally: {err.splitlines()[-1] if err else 'unknown error'}")
        
        # Verify Python setup
        info("Verifying Python setup...")
        result = run_command(['uv', 'python', 'find'])
        if result and result.returncode == 0 and result.stdout.strip():
            default_python = result.stdout.strip()
            success(f"Default Python: {default_python}")
            
            if ".local/share/uv" in default_python:
                success("Using uv-managed Python ✓")
            else:
                warning("Not using uv-managed Python - restart shell to fix")
        else:
            warning("No default Python found via uv")
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
    
    print(f"{Colors.YELLOW}⚠️  IMPORTANT: UV Python Path Configuration{Colors.RESET}")
    print("After installation, you need to restart your shell or run:")
    print("  source ~/.zshrc")
    print()
    print("To verify UV Python is working correctly:")
    print("  python --version                  # Should show uv-managed Python")
    print("  which python                      # Should show path in ~/.local/share/uv/")
    print()
    print("If Python still shows system version, run:")
    print("  make uv-python-setup              # Fix UV Python path configuration")
    print()
    print(f"{Colors.GREEN}✨ AUTOMATIC VERSION SWITCHING:{Colors.RESET}")
    print("UV automatically detects .python-version files!")
    print("  echo '3.12' > .python-version     # Create version file")
    print("  cd your-project                   # Python automatically switches to 3.12")
    print("  python --version                  # Shows Python 3.12.x")
    print("  python-current                    # Show current version")
    print()
    
    print("Next steps - Use language versions:")
    print()
    print("  # Python (uv handles everything - no pyenv needed)")
    print("  uv python install 3.11")
    print("  uv python pin 3.11")
    print("  uv python list                    # List installed versions")
    print("  uv venv                           # Create virtual environment")
    print("  uv pip install package           # Install packages")
    print("  uv tool install black             # Install global tools")
    print("  uv run python script.py          # Run with specific Python")
    print("  python --version                  # Should show uv-managed Python")
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
    print("  sdk use java 17.0.13-amzn       # Switch to Corretto 17 (project default)")
    print("  sdk use java 21.0.5-tem         # Switch to Temurin 21")
    print("  sdk default java 17.0.13-amzn   # Set permanent default")
    print()
    print("  # Installed Java ecosystem at ~/.sdkman/candidates/:")
    print("  #   java/17.0.13-amzn/  (Amazon Corretto JDK 17 — matches project Dockerfile)")
    print("  #   java/21.0.5-tem/    (Eclipse Temurin JDK 21 LTS)")
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