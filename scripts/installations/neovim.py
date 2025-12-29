#!/usr/bin/env python3
"""
Neovim Installation and Configuration Script
Sets up Neovim with plugins, Python environment, and proper configuration.
"""

import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Optional


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
    GRAY = '\033[90m'


class NeovimInstaller:
    """Neovim installation and configuration manager"""
    
    def __init__(self):
        self.current_path = Path.cwd()
        self.home = Path.home()
        self.neovim_dir = self.current_path / "neovim"
        self.config_dir = self.home / ".config"
        self.nvim_config = self.config_dir / "nvim"
    
    def info(self, message: str) -> None:
        print(f"[*] {message}")
    
    def success(self, message: str) -> None:
        print(f"[+] {message}")
    
    def fail(self, message: str) -> None:
        print(f"[!] {message}")
        sys.exit(1)
    
    def warning(self, message: str) -> None:
        print(f"[!] {message}")
    
    def run_command(self, cmd: list, description: str = "", capture_output: bool = False) -> Optional[subprocess.CompletedProcess]:
        """Run a command and handle errors"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                check=True
            )
            
            if description:
                self.success(description)
            
            return result
            
        except subprocess.CalledProcessError as e:
            error_msg = f"Command failed: {' '.join(cmd)}"
            if e.stderr:
                error_msg += f"\nError: {e.stderr}"
            self.fail(error_msg)
        except Exception as e:
            self.fail(f"Unexpected error: {e}")
    
    def create_neovim_directory(self) -> None:
        """Create neovim directory structure in dotfiles"""
        self.info("Creating neovim directory in dotfiles ...")
        
        # Create necessary directories
        directories = [
            self.neovim_dir,
            self.neovim_dir / "autoload",
            self.neovim_dir / "plugged"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Check if init.vim exists
        init_vim = self.neovim_dir / "init.vim"
        if init_vim.exists():
            self.info("init.vim already exists")
        else:
            self.info("init.vim not found - please ensure it exists")
    
    def setup_config_symlink(self) -> None:
        """Setup symlink from ~/.config/nvim to dotfiles/neovim"""
        self.info("Preparing Neovim config directory ...")
        
        # Ensure .config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle existing nvim config
        if self.nvim_config.is_symlink():
            self.nvim_config.unlink()
        elif self.nvim_config.is_dir():
            import shutil
            backup_name = f"nvim.backup.{int(time.time())}"
            backup_path = self.config_dir / backup_name
            shutil.move(str(self.nvim_config), str(backup_path))
            self.info(f"Backed up existing nvim config to {backup_name}")
        
        # Create symlink
        self.info("Creating symlink from ~/.config/nvim to dotfiles/neovim ...")
        self.nvim_config.symlink_to(self.neovim_dir)
        self.success(f"Symlinked {self.nvim_config} -> {self.neovim_dir}")
    
    def create_python_environment(self) -> None:
        """Create Python virtual environment for Neovim dependencies"""
        self.info("Creating Python virtual environment for Neovim dependencies using uv ...")
        
        env_dir = self.neovim_dir / "env"
        
        # Remove existing environment
        if env_dir.exists():
            self.info("Removing existing Python environment ...")
            import shutil
            shutil.rmtree(env_dir)
        
        # Create new environment with uv
        self.run_command([
            "uv", "venv", str(env_dir)
        ], "Python virtual environment created")
        
        # Install Python dependencies
        self.info("Installing Neovim Python dependencies using uv ...")
        python_path = env_dir / "bin" / "python"
        
        dependencies = [
            "wheel", "pynvim", "jedi", "psutil", "setproctitle", "yapf", "doq"
        ]
        
        self.run_command([
            "uv", "pip", "install", "--python", str(python_path)
        ] + dependencies, "Neovim Python dependencies installed")
    
    def install_vim_plug(self) -> None:
        """Install vim-plug plugin manager"""
        self.info("Downloading vim-plug, the best minimalistic vim plugin manager ...")
        
        plug_vim = self.neovim_dir / "autoload" / "plug.vim"
        plug_url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"
        
        try:
            # Ensure autoload directory exists
            plug_vim.parent.mkdir(parents=True, exist_ok=True)
            
            # Download vim-plug
            urllib.request.urlretrieve(plug_url, str(plug_vim))
            self.success("vim-plug downloaded successfully")
            
        except Exception as e:
            self.fail(f"Failed to download vim-plug: {e}")
    
    def verify_neovim_available(self) -> None:
        """Verify that neovim is installed and available"""
        try:
            result = subprocess.run(["nvim", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                self.success(f"Neovim available: {version_line}")
            else:
                self.fail("Neovim is not properly installed")
        except FileNotFoundError:
            self.fail("Neovim is not installed. Please install it first with: brew install neovim")
    
    def install_plugins(self) -> None:
        """Install Neovim plugins using vim-plug"""
        self.info("Running :PlugInstall within nvim ...")
        
        try:
            # Run neovim in headless mode to install plugins
            result = subprocess.run([
                "nvim", "--headless", "-c", ":PlugInstall", "-c", ":UpdateRemotePlugins", "-c", ":qall"
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode == 0:
                self.success("Neovim plugins installed successfully")
            else:
                self.warning("Plugin installation may have encountered issues")
                if result.stderr:
                    print(f"Error output: {result.stderr}")
                    
        except subprocess.TimeoutExpired:
            self.warning("Plugin installation timed out - some plugins may not be installed")
        except Exception as e:
            self.warning(f"Plugin installation failed: {e}")
    
    def verify_installation(self) -> bool:
        """Verify that Neovim is properly set up"""
        self.info("Verifying Neovim installation...")
        
        checks = [
            (self.nvim_config.is_symlink(), "Config symlink created"),
            ((self.neovim_dir / "env").exists(), "Python environment created"),
            ((self.neovim_dir / "autoload" / "plug.vim").exists(), "vim-plug installed"),
            ((self.neovim_dir / "plugged").exists(), "Plugins directory created"),
        ]
        
        all_good = True
        for check, description in checks:
            if check:
                self.success(description)
            else:
                self.warning(f"Failed: {description}")
                all_good = False
        
        return all_good
    
    def install_neovim(self) -> None:
        """Complete Neovim installation process"""
        print("")
        print(f"{Colors.GRAY}###################################")
        print(f"# scripts/installations/neovim.py #")
        print(f"###################################{Colors.RESET}")
        print("")
        print("### Neovim config setting and plugins installing...")
        
        # Step 1: Create neovim directory structure
        self.create_neovim_directory()
        
        # Step 2: Setup config symlink
        self.setup_config_symlink()
        
        # Step 3: Create Python environment
        self.create_python_environment()
        
        # Step 4: Install vim-plug
        self.install_vim_plug()
        
        # Step 5: Verify neovim is available
        self.verify_neovim_available()
        
        # Step 6: Install plugins
        self.install_plugins()
        
        # Final messages
        print(f"[+] Done, welcome to {Colors.BOLD}{Colors.GREEN}NeoVim{Colors.RESET}! Try it by running: nvim")
        print(f"[+] Configuration location: {self.neovim_dir}/")
        print(f"[+] Symlinked to: {self.nvim_config} -> {self.neovim_dir}")
        print(f"[+] Want to customize it? Modify {self.neovim_dir}/init.vim")
        print("### Neovim config setting and plugins installing... done !!")
        
        print("")
        print(f"{Colors.GREEN}# scripts/installations/neovim.py Finish !!{Colors.RESET}")
        print("")


def main():
    """Main function"""
    installer = NeovimInstaller()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--verify":
            success = installer.verify_installation()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--help":
            print("Neovim Installation Script")
            print("Usage:")
            print("  python neovim.py          # Install and configure Neovim")
            print("  python neovim.py --verify # Verify installation")
            return
    
    try:
        installer.install_neovim()
        
        # Verify installation
        if installer.verify_installation():
            print(f"[ {Colors.GREEN}OK{Colors.RESET} ] Neovim successfully installed and configured!")
        else:
            print(f"[ {Colors.YELLOW}WARN{Colors.RESET} ]Neovim installation completed with some warnings")
            
    except KeyboardInterrupt:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ {Colors.RED}FAIL{Colors.RESET} ] Installation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()