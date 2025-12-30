# Modern Development Environment Setup

A comprehensive, automated development environment setup for macOS with modern tooling and best practices.

## 🚀 Quick Start

### Prerequisites

1. **Install Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

2. **Setup GitHub SSH Key**
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
   cat ~/.ssh/id_rsa.pub
   ```
   Add the key to your [GitHub SSH Keys](https://github.com/settings/keys)

3. **Clone Repository**
   ```bash
   git clone git@github.com:valhein256/dotfiles.git
   cd dotfiles
   ```

### One-Command Installation

```bash
make install
```

This orchestrated installation includes:
- 📦 Homebrew packages (70+ modern development tools)
- 🔧 Language managers (Python, Node.js, Java, Rust, Go)
- ⚙️ Dotfiles configuration
- 📝 Neovim plugins
- 🔗 Git submodules

## 📊 System Status & Verification

### Check Installation Status
```bash
make system-status                    # Check if everything is properly installed
make system-status-installed          # Explicit installation verification
make install-verify                   # Detailed installation verification
```

### Check Cleanup Status
```bash
make system-status-cleaned            # Verify system is clean after cleanup
make cleanup-verify                   # Detailed cleanup verification
```

## 🧹 System Management

### Complete System Reset
```bash
make full-reset                       # Clean everything and reinstall
```

### Selective Operations
```bash
make clean                           # Remove all components
make install-packages                # Install only Homebrew packages
make install-dotfiles                # Install only dotfiles
make install-language-managers       # Install only language managers
```

## 📦 Package Management

### Modern Language Ecosystems

Our setup uses industry best practices with modern, fast tools:

| Language | Tool | Replaces | Benefits |
|----------|------|----------|----------|
| **Python** | `uv` | pyenv + pip + poetry + pipx | 10-100x faster, unified tool |
| **Node.js** | `fnm` | nvm | 40x faster, cross-platform |
| **Java** | `SDKMAN` | Manual management | Multiple JDK versions, instant switching |
| **Rust** | `rustup` | Manual management | Official toolchain manager |
| **Go** | `go` | Manual management | Official version management |

### Package Categories

```bash
# View all available packages
python3 scripts/installations/packages.py list

# Install by category
make install-packages                 # All packages
python3 scripts/installations/packages.py install --category python
python3 scripts/installations/packages.py install --category nodejs
python3 scripts/installations/packages.py install --category golang
```

**Available Categories:**
- `core` - Essential system tools (zsh, git, tree, fzf, ripgrep)
- `editor` - Development editors (neovim, universal-ctags)
- `python` - Python ecosystem (uv - replaces pyenv + pip + poetry + pipx)
- `nodejs` - Node.js ecosystem (fnm, pnpm - fnm is 40x faster than nvm)
- `golang` - Go ecosystem (official go toolchain)
- `java-prereq` - Java prerequisites (zip, unzip, curl for SDKMAN)
- `rust` - Rust ecosystem (rustup official toolchain)
- `devops` - DevOps tools (kubectl, helm, terraform, terragrunt)
- `cloud` - Cloud tools (awscli, gcloud-cli)
- `network` - Network tools (openssh, sshs, teleport)
- `terminal` - Terminal tools (tmux)
- `fonts` - Development fonts (SauceCodePro Nerd Font)
- `system` - System tools (xquartz)
- `optional` - Optional tools (ansible, kind)

## 🔧 Language Version Management

### Automatic Version Switching

Our setup supports automatic version switching based on project configuration files:

| Language | File | Example | Auto-Switch |
|----------|------|---------|-------------|
| **Python** | `.python-version` | `3.12` | ✅ Automatic with UV |
| **Node.js** | `.nvmrc` | `18` | ✅ Automatic with fnm |
| **Java** | Manual switching | `sdk use java 21.0.1-tem` | Manual with SDKMAN |

### Python - UV (Modern All-in-One Tool)

**Important**: After installation, restart your shell or run `source ~/.zshrc` to activate uv Python path management.

**✨ Automatic Version Switching**: UV automatically detects `.python-version` files and switches Python versions when you change directories!

```bash
# Verify uv Python is working
python --version                      # Should show uv-managed Python
which python                          # Should show path in ~/.local/share/uv/

# If still showing system Python, fix the configuration:
make uv-python-setup                  # Configure UV Python environment

# Install Python versions
uv python install 3.12
uv python install 3.11
uv python list

# Automatic version switching with .python-version files
echo "3.12" > .python-version         # Create version file
cd your-project                       # Python automatically switches to 3.12!
python --version                      # Shows Python 3.12.x
python-current                        # Show current version (alias)

# Project management (replaces poetry)
uv init my-project
cd my-project
uv add fastapi uvicorn
uv run python main.py

# Global tools (replaces pipx)
uv tool install black
uv tool install pytest
uv tool install ruff

# Virtual environments (replaces venv)
uv venv                               # Create virtual environment
source .venv/bin/activate             # Activate (or use uv run)
uv run python script.py              # Run without activation
```

### Node.js - FNM (40x Faster than NVM)
```bash
# Install and use Node.js versions
fnm install --lts
fnm use lts-latest
fnm default lts-latest
fnm list

# Package management with pnpm (faster than npm)
pnpm install
pnpm add express
pnpm run dev
```

### Java - SDKMAN (Multi-Version Management)
```bash
# After installation, restart shell and run:
source ~/.sdkman/bin/sdkman-init.sh

# Install and switch JDK versions
sdk list java
sdk install java 21.0.1-tem
sdk install java 17.0.9-tem
sdk use java 21.0.1-tem          # Switch for current session
sdk default java 21.0.1-tem      # Set permanent default

# Build tools
sdk install maven
sdk install gradle
```

### Rust - Rustup (Official Toolchain)
```bash
# After installation:
source ~/.cargo/env
rustup update stable
rustup install nightly
rustup default stable
```

### Go - Official Toolchain
```bash
# Go is installed via Homebrew with latest version
go version
go mod init my-project
go get github.com/gin-gonic/gin
```

## 🍺 Homebrew Management

### Package Installation
```bash
make brew-install PACKAGE=git
make brew-install PACKAGE=docker CASK=true    # GUI applications
```

### Custom Formulas
```bash
make brew-list-formulas                        # List available custom formulas
make brew-install-formula FORMULA=formulas/teleport.rb
```

### Maintenance
```bash
make brew-update                               # Update Homebrew
make brew-upgrade                              # Upgrade all packages
make brew-clean-taps                           # Remove custom taps
```

## 🏠 Local Taps Management

```bash
make local-taps-list                           # List local taps
make local-taps-backup DIR=backup-dir          # Backup taps
make local-taps-restore DIR=backup-dir         # Restore taps
make local-taps-validate                       # Validate taps
```

## ⚙️ Configuration

### Font Setup
The setup automatically installs **SauceCodePro Nerd Font**. Configure your terminal:

**iTerm2**: Settings → Profiles → Text → Font: SauceCodePro Nerd Font

### Theme Setup
1. Download themes from [iTerm2 Color Schemes](https://iterm2colorschemes.com/)
2. Import: iTerm2 Settings → Profiles → Colors → Color Presets → Import
3. Recommended: Hurtado theme

### Git Configuration
```bash
# Global configuration
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"

# Per-project configuration
git config --local user.name "Your Name"
git config --local user.email "work-email@company.com"
```

## 🔍 Troubleshooting

### System Status Check
```bash
make system-status                             # Comprehensive status check
make system-status CHECK_TYPE=installed       # Check installation status
make system-status CHECK_TYPE=cleaned         # Check cleanup status
```

### Common Issues

**Empty directories in tmux/zsh:**
```bash
make full-reset                                # Complete reset and reinstall
tree -L 2 zsh                                 # Verify zsh structure
tree -L 3 tmux                                # Verify tmux structure
```

**Permission issues:**
```bash
sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions
```

**ZSH completion errors (_arguments:327: comparguments):**

This error occurs when the `comparguments` function is missing. Here are solutions in order of preference:

```bash
# Method 1: Comprehensive fix (recommended)
make fix-zsh-completion                        # Fix completion system
exec $SHELL -l                                # Restart shell

# Method 2: Simple fix (faster)
make fix-zsh-simple                            # Quick fix
exec $SHELL -l                                # Restart shell

# Method 3: Manual fix (if make commands fail)
rm -f ~/.zcompdump*                            # Clear completion cache
autoload -Uz compinit && compinit              # Reinitialize
exec $SHELL -l                                # Restart shell
```

**Root causes:**
- Missing `comparguments` function in system zsh
- Corrupted completion cache files
- Plugin loading conflicts

**ZSH completion errors (_arguments:327: comparguments):**

**Language manager not working:**
```bash
# Restart shell after installation
exec $SHELL -l

# Check specific language manager
uv --version                                   # Python
fnm --version                                  # Node.js
sdk version                                    # Java (after sourcing SDKMAN)
rustup --version                              # Rust
go version                                     # Go
```

**UV Python not working (still using system Python):**
```bash
# Check current Python
python --version                               # Should show uv-managed version
which python                                   # Should show ~/.local/share/uv/ path

# Fix UV Python configuration
make uv-python-setup                           # Configure UV environment
source ~/.zshrc                                # Reload shell configuration

# Verify UV Python versions
uv python list                                 # List installed versions
uv python find                                 # Show current default Python

# Install Python if none available
uv python install 3.12                        # Install Python 3.12
uv python pin 3.12                            # Set as default
```

**Python version not switching with .python-version files:**
```bash
# Check if .python-version file is detected
uv python find --show-version                 # Should show version from file
uv python find                                # Should show path to that version

# Create .python-version file manually
echo "3.12" > .python-version                 # Create version file
uv python install 3.12                        # Install if not available
cd .                                           # Trigger directory change
python --version                               # Should show Python 3.12.x

# Check available aliases
python-current                                 # Show current version
python-which                                   # Show current Python path
python-versions                               # List all installed versions
```

## 🛠️ Advanced Usage

### Development & Testing
```bash
make build                                     # Build test environment
make container-bash                            # Run bash in container
```

### Selective Component Management
```bash
# Individual component installation
make install-packages
make install-dotfiles
make install-language-managers
make install-neovim
make install-git-submodules

# Individual component cleanup
make clean-packages
make clean-dotfiles
make clean-language-managers
make clean-neovim
make clean-caches
```

### Legacy Compatibility
```bash
# Legacy commands (still supported)
make packages                                  # Same as install-packages
make language-managers                         # Same as install-language-managers
make dotfiles                                  # Same as install-dotfiles
make neovim-plugins                           # Same as install-neovim
```

## 📚 Architecture

This setup follows modern development best practices:

- **Orchestrated Installation**: Single command installs everything in correct order
- **Comprehensive Verification**: Status checks ensure everything works correctly
- **Modern Tooling**: Uses fastest, most reliable tools for each language
- **Modular Design**: Install/remove components independently
- **Automated Cleanup**: Complete system reset capability
- **Cross-Platform**: Works on Intel and Apple Silicon Macs

## 🔗 References

- [Homebrew](https://brew.sh/) - Package manager for macOS
- [UV Python](https://github.com/astral-sh/uv) - Modern Python package manager
- [FNM](https://github.com/Schniz/fnm) - Fast Node.js version manager
- [SDKMAN](https://sdkman.io/) - Java ecosystem manager
- [iTerm2](https://iterm2.com/) - Terminal emulator
- [Neovim](https://neovim.io/) - Modern Vim editor

---

**Quick Commands Reference:**
- `make install` - Install everything
- `make system-status` - Check status
- `make full-reset` - Reset and reinstall
- `make help` - Show all available commands
