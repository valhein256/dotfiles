##@ Helpers

.PHONY: help

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) && echo

##@ MAIN OPERATIONS

install: ## 🚀 Complete installation (orchestrated)
	@echo ""
	@printf "\033[95m##########################################\033[0m\n"
	@printf "\033[95m# 🚀 COMPLETE SYSTEM INSTALLATION 🚀   #\033[0m\n"
	@printf "\033[95m##########################################\033[0m\n"
	@echo ""
	@echo "This will install all development environment components:"
	@echo ""
	@echo "  🏠 Local Taps - Restore custom Homebrew taps from backup"
	@echo "  📦 Homebrew Packages - Install all formulae, casks, and custom formulas"
	@echo "  🔄 Package Updates - Update all installed packages to latest versions"
	@echo "  🔗 Git Submodules - Initialize zplug and tmux plugins"
	@echo "  ⚙️  Dotfiles - Create symlinks for all configuration files"
	@echo "  🔧 Language Managers - Setup Python, Node.js, Java, Rust, Go"
	@echo "  📝 Neovim Plugins - Install and configure Neovim plugins"
	@echo ""
	@echo "  ✅ All configurations will be properly linked"
	@echo "  ✅ All packages will be updated to latest versions"
	@echo "  ✅ Development environment will be ready to use"
	@echo ""
	@printf "\033[92m🎯 This will set up your complete development environment!\033[0m\n"
	@echo ""
	@echo -n "❓ Proceed with complete installation? Type 'INSTALL' to confirm: "; \
	read confirm; \
	if [ "$confirm" != "INSTALL" ]; then \
		echo "❌ Operation cancelled"; \
		exit 1; \
	fi
	@echo ""
	@printf "\033[94mStarting complete system installation...\033[0m\n"
	@echo ""
	@$(MAKE) install-step-1-local-taps
	@$(MAKE) install-step-2-packages
	@$(MAKE) install-step-3-brew-upgrade
	@$(MAKE) install-step-4-git-submodules  
	@$(MAKE) install-step-5-dotfiles
	@$(MAKE) install-step-6-language-managers
	@$(MAKE) install-step-7-neovim
	@echo ""
	@printf "\033[92m✅ Complete system installation finished!\033[0m\n"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run: make install-verify"
	@echo "  2. Run: make system-status"
	@echo "  3. Test your development environment"
	@echo ""
	@echo "🎉 Your development environment should now be ready!"

clean: ## 🧹 Complete cleanup (orchestrated)
	@echo ""
	@printf "\033[91m##########################################\033[0m\n"
	@printf "\033[91m# 🧹 COMPLETE SYSTEM CLEANUP 🧹         #\033[0m\n"
	@printf "\033[91m##########################################\033[0m\n"
	@echo ""
	@echo "This will run specialized cleanup scripts:"
	@echo ""
	@echo "  🍺 Homebrew Packages - Remove all formulae, casks, and custom taps"
	@echo "  🔧 Language Managers - Remove Python, Node.js, Java, Rust, Go"
	@echo "  📝 Neovim Dynamic Content - Remove plugins and cache"
	@echo "  ⚙️  Dotfiles - Remove all symlinks"
	@echo "  🏠 Local Taps - Backup and remove custom Homebrew taps"
	@echo "  🔗 Git Submodules - Deinitialize and remove submodules"
	@echo "  🗑️  Caches - Remove all development caches"
	@echo ""
	@echo "  ✅ Original config files will be preserved"
	@echo "  ✅ Backups will be created before removal"
	@echo ""
	@printf "\033[93m⚠️  WARNING: This will remove ALL development tools and data!\033[0m\n"
	@echo ""
	@echo -n "❓ Are you ABSOLUTELY SURE you want to proceed? Type 'CLEANUP' to confirm: "; \
	read confirm; \
	if [ "$confirm" != "CLEANUP" ]; then \
		echo "❌ Operation cancelled"; \
		exit 1; \
	fi
	@echo ""
	@printf "\033[94mStarting complete system cleanup...\033[0m\n"
	@echo ""
	@$(MAKE) clean-step-1-brew-packages
	@$(MAKE) clean-step-2-language-managers
	@$(MAKE) clean-step-3-neovim
	@$(MAKE) clean-step-4-dotfiles
	@$(MAKE) clean-step-5-local-taps
	@$(MAKE) clean-step-6-git-submodules
	@$(MAKE) clean-step-7-caches
	@echo ""
	@printf "\033[92m✅ Complete system cleanup finished!\033[0m\n"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run: make cleanup-verify"
	@echo "  2. If verification passes, run: make install"
	@echo "  3. Run: make install-verify"
	@echo ""
	@echo "Your backups are saved in the backups/ directory"

full-reset: ## 🔄 Complete reset and reinstall (clean + install)
	@echo ""
	@printf "\033[94m##########################################\033[0m\n"
	@printf "\033[94m# 🔄 FULL SYSTEM RESET & REINSTALL 🔄  #\033[0m\n"
	@printf "\033[94m##########################################\033[0m\n"
	@echo ""
	@echo "This will completely clean the system and reinstall everything:"
	@echo ""
	@echo "  🧹 CLEANUP PHASE:"
	@echo "    🍺 Remove all Homebrew packages and custom taps"
	@echo "    🔧 Remove all language managers"
	@echo "    📝 Remove Neovim dynamic content"
	@echo "    ⚙️  Remove all dotfiles symlinks"
	@echo "    🏠 Remove local Homebrew taps"
	@echo "    🔗 Remove git submodules"
	@echo "    🗑️  Remove all development caches"
	@echo ""
	@echo "  🚀 INSTALLATION PHASE:"
	@echo "    🏠 Restore local Homebrew taps"
	@echo "    📦 Install all Homebrew packages"
	@echo "    🔄 Update all packages to latest versions"
	@echo "    🔗 Initialize git submodules"
	@echo "    ⚙️  Create dotfiles symlinks"
	@echo "    🔧 Setup language managers"
	@echo "    📝 Install Neovim plugins"
	@echo ""
	@echo "  ✅ Backups will be created before removal"
	@echo "  ✅ All packages will be updated to latest versions"
	@echo "  ✅ Complete development environment will be restored"
	@echo ""
	@printf "\033[93m⚠️  WARNING: This will remove ALL current installations and reinstall everything!\033[0m\n"
	@echo ""
	@echo -n "❓ Are you ABSOLUTELY SURE you want to proceed? Type 'RESET' to confirm: "; \
	read confirm; \
	if [ "$confirm" != "RESET" ]; then \
		echo "❌ Operation cancelled"; \
		exit 1; \
	fi
	@echo ""
	@printf "\033[91m🧹 PHASE 1: Starting complete system cleanup...\033[0m\n"
	@echo ""
	@$(MAKE) clean-step-1-brew-packages
	@$(MAKE) clean-step-2-language-managers
	@$(MAKE) clean-step-3-neovim
	@$(MAKE) clean-step-4-dotfiles
	@$(MAKE) clean-step-5-local-taps
	@$(MAKE) clean-step-6-git-submodules
	@$(MAKE) clean-step-7-caches
	@echo ""
	@printf "\033[92m✅ Cleanup phase completed successfully!\033[0m\n"
	@echo ""
	@printf "\033[94m🚀 PHASE 2: Starting complete system installation...\033[0m\n"
	@echo ""
	@$(MAKE) install-step-1-local-taps
	@$(MAKE) install-step-2-packages
	@$(MAKE) install-step-3-brew-upgrade
	@$(MAKE) install-step-4-git-submodules  
	@$(MAKE) install-step-5-dotfiles
	@$(MAKE) install-step-6-language-managers
	@$(MAKE) install-step-7-neovim
	@echo ""
	@printf "\033[92m✅ Installation phase completed successfully!\033[0m\n"
	@echo ""
	@printf "\033[95m🎉 FULL RESET COMPLETE! 🎉\033[0m\n"
	@echo ""
	@echo "Running final verification..."
	@$(MAKE) install-verify
	@echo ""
	@echo "🎯 Your development environment has been completely reset and reinstalled!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run: make system-status"
	@echo "  2. Test your development environment"
	@echo "  3. Check backups in the backups/ directory if needed"

##@ VERIFICATION & STATUS

system-status: ## 📊 Check comprehensive system status
	@chmod +x ./scripts/verifications/system-status-checker.py
	@echo "📊 System Status Check"
	@echo "CHECK_TYPE: default (installation status)"
	@echo ""
	@./scripts/verifications/system-status-checker.py

install-verify: ## ✅ Verify installation completeness
	@chmod +x ./scripts/verifications/installation-verification.py
	@./scripts/verifications/installation-verification.py

cleanup-verify: ## ✅ Verify cleanup completeness
	@chmod +x ./scripts/verifications/cleanup-verification.py
	@./scripts/verifications/cleanup-verification.py

##@ COMPONENT INSTALLATION

install-packages: ## 📦 Install Homebrew packages only
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all

install-updates: ## 🔄 Install only missing/new packages (skip already installed)
	@echo "🔄 Installing missing and newly added packages..."
	@echo ""
	@echo "This will:"
	@echo "  ✅ Skip packages that are already installed"
	@echo "  📦 Install only missing or newly added packages"
	@echo "  🧹 Clean up obsolete packages with modern replacements"
	@echo ""
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all
	@echo ""
	@echo "✅ Package updates completed!"
	@echo ""
	@echo "💡 To see what was installed, run: make system-status"

install-and-upgrade: ## 🚀 Install missing packages AND upgrade all existing packages
	@echo "🚀 Installing missing packages and upgrading existing ones..."
	@echo ""
	@echo "This will:"
	@echo "  📦 Install any missing or newly added packages"
	@echo "  🔄 Upgrade all existing packages to latest versions"
	@echo "  🧹 Clean up obsolete packages and old versions"
	@echo ""
	@echo "⏱️  This may take several minutes depending on updates available"
	@echo ""
	@printf "❓ Proceed with install and upgrade? [y/N]: "; \
	read confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo ""; \
		echo "📦 Step 1: Installing missing packages..."; \
		chmod +x ./scripts/installations/packages.py; \
		./scripts/installations/packages.py install --all; \
		echo ""; \
		echo "🔄 Step 2: Upgrading all existing packages..."; \
		$(MAKE) brew-upgrade; \
		echo ""; \
		echo "✅ Install and upgrade completed!"; \
		echo ""; \
		echo "📊 Summary:"; \
		echo "  • Missing packages have been installed"; \
		echo "  • All packages upgraded to latest versions"; \
		echo "  • Old package versions cleaned up"; \
		echo ""; \
		echo "💡 Run 'make system-status' to verify everything is working"; \
	else \
		echo "❌ Operation cancelled"; \
		exit 1; \
	fi

install-and-upgrade-force: ## 🚀 Install missing packages AND upgrade all existing packages (no confirmation)
	@echo "🚀 Installing missing packages and upgrading existing ones..."
	@echo ""
	@echo "📦 Step 1: Installing missing packages..."
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all
	@echo ""
	@echo "🔄 Step 2: Upgrading all existing packages..."
	@$(MAKE) brew-upgrade
	@echo ""
	@echo "✅ Install and upgrade completed!"
	@echo ""
	@echo "📊 Summary:"
	@echo "  • Missing packages have been installed"
	@echo "  • All packages upgraded to latest versions"
	@echo "  • Old package versions cleaned up"
	@echo ""
	@echo "💡 Run 'make system-status' to verify everything is working"

sync-packages: ## ⚡ Quick sync - install missing packages and upgrade existing (no confirmation)
	@echo "⚡ Quick package sync..."
	@echo ""
	@echo "📦 Installing missing packages..."
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all
	@echo ""
	@echo "🔄 Upgrading existing packages..."
	@$(MAKE) brew-upgrade
	@echo ""
	@echo "✅ Package sync completed!"

install-category: ## 📂 Install packages by category (usage: make install-category CATEGORY=ai-tools)
	@if [ -z "$(CATEGORY)" ]; then \
		echo "Usage: make install-category CATEGORY=category-name"; \
		echo ""; \
		echo "Available categories:"; \
		python3 scripts/installations/packages.py list | grep "📂" | sed 's/📂 //g'; \
		exit 1; \
	fi
	@echo "📂 Installing $(CATEGORY) packages..."
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --category $(CATEGORY)

packages-status: ## 📊 Show package installation status
	@echo "📊 Package Installation Status"
	@echo "=============================="
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py status

install-dotfiles: ## ⚙️ Install dotfiles symlinks only
	@chmod +x ./scripts/installations/dotfiles.py
	@./scripts/installations/dotfiles.py

install-language-managers: ## 🔧 Install language managers only
	@chmod +x ./scripts/installations/language-managers.py
	@./scripts/installations/language-managers.py

install-neovim: ## 📝 Install Neovim plugins only
	@chmod +x ./scripts/installations/neovim.py
	@./scripts/installations/neovim.py

install-git-submodules: ## 🔗 Install git submodules only
	@chmod +x ./scripts/installations/git-submodule.py
	@./scripts/installations/git-submodule.py

install-local-taps: ## 🏠 Restore local Homebrew taps
	@chmod +x ./scripts/installations/local-taps-manager.py
	@if [ -d "./backups/local-taps" ]; then \
		./scripts/installations/local-taps-manager.py restore ./backups/local-taps; \
	else \
		echo "No local taps backup found, skipping..."; \
	fi

##@ COMPONENT CLEANUP

clean-packages: ## 🍺 Remove Homebrew packages only
	@chmod +x ./scripts/cleanup/brew-packages.py
	@./scripts/cleanup/brew-packages.py

clean-dotfiles: ## ⚙️ Remove dotfiles symlinks only
	@chmod +x ./scripts/cleanup/dotfiles.py
	@./scripts/cleanup/dotfiles.py

clean-language-managers: ## 🔧 Remove language managers only
	@chmod +x ./scripts/cleanup/language-managers.py
	@./scripts/cleanup/language-managers.py

clean-neovim: ## 📝 Remove Neovim content only
	@chmod +x ./scripts/cleanup/neovim.py
	@./scripts/cleanup/neovim.py

clean-local-taps: ## 🏠 Remove local Homebrew taps
	@chmod +x ./scripts/cleanup/local-taps.py
	@./scripts/cleanup/local-taps.py

clean-git-submodules: ## 🔗 Remove git submodules only
	@chmod +x ./scripts/cleanup/git-submodules.py
	@./scripts/cleanup/git-submodules.py

clean-caches: ## 🗑️ Remove development caches only
	@chmod +x ./scripts/cleanup/caches.py
	@./scripts/cleanup/caches.py

##@ SYSTEM FIXES

fix-zsh-completion: ## 🔧 Fix ZSH completion system (resolve _arguments errors)
	@echo "🔧 Enhanced ZSH completion system fix..."
	@echo ""
	@echo "Step 1: Clearing completion cache and problematic files..."
	@rm -f ~/.zcompdump* ~/.zsh/cache/* ~/.zplug/cache/* 2>/dev/null || true
	@rm -f ~/.zsh/.zcompdump* 2>/dev/null || true
	@echo "✅ Cache cleared"
	@echo ""
	@echo "Step 2: Creating necessary directories..."
	@mkdir -p ~/.zsh/{cache,functions} 2>/dev/null || true
	@echo "✅ Directories created"
	@echo ""
	@echo "Step 3: Installing completion function fixes..."
	@echo '#!/bin/zsh\n# Stub function to prevent _arguments errors\n_arguments() { _files }' > ~/.zsh/functions/_arguments
	@echo '#!/bin/zsh\n# Stub function to prevent comparguments errors\ncomparguments() { return 0 }' > ~/.zsh/functions/comparguments
	@chmod +x ~/.zsh/functions/_arguments ~/.zsh/functions/comparguments
	@echo "✅ Function stubs installed"
	@echo ""
	@echo "Step 4: Resetting completion system with proper fpath..."
	@zsh -c 'fpath=(~/.zsh/functions /opt/homebrew/share/zsh/site-functions $$fpath) && autoload -Uz compinit && compinit -d ~/.zcompdump -C'
	@echo "✅ Completion system reset"
	@echo ""
	@echo "Step 5: Verifying fix..."
	@zsh -c 'autoload -Uz _arguments comparguments && echo "Functions loaded successfully"' || echo "⚠️  Some functions may still have issues"
	@echo ""
	@echo "✅ ZSH completion system fixed!"
	@echo ""
	@echo "🔄 Please restart your shell: exec \$$SHELL -l"
	@echo "🧪 Test with: git <TAB> or make <TAB>"

uv-python-setup: ## 🐍 Configure UV Python environment with .python-version support
	@echo "🐍 Configuring UV Python environment..."
	@echo ""
	@echo "Checking UV installation..."
	@uv --version || (echo "❌ UV not installed. Run 'make install-packages' first." && exit 1)
	@echo ""
	@echo "Installing Python 3.12 if not available..."
	@uv python install 3.12 2>/dev/null || echo "✅ Python 3.12 already available"
	@echo ""
	@echo "Setting Python 3.12 as default..."
	@uv python pin 3.12 2>/dev/null || echo "✅ Python 3.12 already set as default"
	@echo ""
	@echo "Checking for fswatch (for .python-version file monitoring)..."
	@if ! command -v fswatch &> /dev/null; then \
		echo "📦 Installing fswatch for file monitoring..."; \
		brew install fswatch || echo "⚠️  Failed to install fswatch, will use periodic checking instead"; \
	else \
		echo "✅ fswatch already installed"; \
	fi
	@echo ""
	@echo "Creating UV Python shims..."
	@mkdir -p ~/.local/share/uv/shims
	@echo '#!/bin/bash\nuv_python=$$(uv python find 2>/dev/null)\nif [ -n "$$uv_python" ]; then\n    exec "$$uv_python" "$$@"\nelse\n    exec /opt/homebrew/bin/python3 "$$@" 2>/dev/null || exec /usr/bin/python3 "$$@"\nfi' > ~/.local/share/uv/shims/python
	@echo '#!/bin/bash\nuv_python=$$(uv python find 2>/dev/null)\nif [ -n "$$uv_python" ]; then\n    exec "$$uv_python" "$$@"\nelse\n    exec /opt/homebrew/bin/python3 "$$@" 2>/dev/null || exec /usr/bin/python3 "$$@"\nfi' > ~/.local/share/uv/shims/python3
	@echo '#!/bin/bash\nuv_python=$$(uv python find 2>/dev/null)\nif [ -n "$$uv_python" ]; then\n    exec "$$uv_python" -m pip "$$@"\nelse\n    exec /opt/homebrew/bin/python3 -m pip "$$@" 2>/dev/null || exec /usr/bin/python3 -m pip "$$@"\nfi' > ~/.local/share/uv/shims/pip
	@echo '#!/bin/bash\nuv_python=$$(uv python find 2>/dev/null)\nif [ -n "$$uv_python" ]; then\n    exec "$$uv_python" -m pip "$$@"\nelse\n    exec /opt/homebrew/bin/python3 -m pip "$$@" 2>/dev/null || exec /usr/bin/python3 -m pip "$$@"\nfi' > ~/.local/share/uv/shims/pip3
	@chmod +x ~/.local/share/uv/shims/{python,python3,pip,pip3}
	@echo "✅ UV Python shims created"
	@echo ""
	@echo "Current UV Python status:"
	@echo "  Default Python: $(uv python find 2>/dev/null || echo 'Not found')"
	@echo "  Python version: $(uv python find --show-version 2>/dev/null || echo 'Not found')"
	@echo "  Shims directory: ~/.local/share/uv/shims"
	@echo "  File monitoring: $$(command -v fswatch &> /dev/null && echo 'fswatch available' || echo 'periodic checking')"
	@echo ""
	@echo "✅ UV Python configuration complete!"
	@echo ""
	@echo "🔄 Please restart your shell: exec \$$SHELL -l"
	@echo "   Then test with: which python3 && python --version"

python-refresh: ## 🔄 Manually refresh Python version (useful after editing .python-version)
	@echo "🔄 Refreshing Python version detection..."
	@if [ -f ".python-version" ]; then \
		echo "📝 Found .python-version: $$(cat .python-version)"; \
		echo "🐍 Current UV Python: $$(uv python find --show-version 2>/dev/null || echo 'Not found')"; \
		uv python pin "$$(cat .python-version)" 2>/dev/null || echo "⚠️  Python $$(cat .python-version) not installed"; \
		echo "✅ Python version refreshed"; \
		echo "🧪 Testing: $$(python --version 2>/dev/null || echo 'Python not found')"; \
	else \
		echo "❌ No .python-version file found in current directory"; \
	fi

install-claude-code: ## 🤖 Install Claude Code CLI (Anthropic's AI coding assistant)
	@echo "🤖 Installing Claude Code CLI..."
	@echo ""
	@echo "Claude Code is Anthropic's terminal-based AI coding assistant"
	@echo "that works directly in your development environment."
	@echo ""
	@echo "Installing via Homebrew cask..."
	@brew install --cask claude-code || (echo "❌ Failed to install Claude Code" && exit 1)
	@echo ""
	@echo "✅ Claude Code installed successfully!"
	@echo ""
	@echo "🚀 Getting started:"
	@echo "  1. Run: claude auth"
	@echo "  2. Follow the authentication process"
	@echo "  3. Navigate to your project: cd your-project"
	@echo "  4. Start Claude Code: claude"
	@echo ""
	@echo "💡 Authentication options:"
	@echo "  • Claude Console (default) - Requires active billing"
	@echo "  • Claude Pro/Max subscription - Unified subscription"
	@echo "  • Enterprise platforms - Bedrock, Vertex AI, Foundry"
	@echo ""
	@echo "📚 Learn more: https://docs.claude.com/en/docs/claude-code/overview"

##@ HOMEBREW MANAGEMENT

brew-install: ## 🍺 Install package (usage: make brew-install PACKAGE=git)
	@if [ -z "$(PACKAGE)" ]; then \
		echo "Usage: make brew-install PACKAGE=package-name [CASK=true]"; \
		exit 1; \
	fi
	@chmod +x ./scripts/installations/brew-manager.py
	@if [ "$(CASK)" = "true" ]; then \
		./scripts/installations/brew-manager.py install --cask "$(PACKAGE)"; \
	else \
		./scripts/installations/brew-manager.py install "$(PACKAGE)"; \
	fi

brew-upgrade: ## 🔄 Upgrade all installed packages to latest versions
	@echo "🔄 Updating Homebrew package database..."
	@brew update
	@echo "📦 Upgrading all installed packages to latest versions..."
	@brew upgrade --greedy
	@echo "🧹 Cleaning up old package versions..."
	@brew cleanup
	@echo "✅ All packages updated to latest versions!"

##@ LOCAL TAPS MANAGEMENT

local-taps-list: ## 🏠 List all local Homebrew taps
	@chmod +x ./scripts/installations/local-taps-manager.py
	@./scripts/installations/local-taps-manager.py list

local-taps-backup: ## 🏠 Backup local taps (usage: make local-taps-backup DIR=backup-dir)
	@if [ -z "$(DIR)" ]; then \
		echo "Usage: make local-taps-backup DIR=backup-directory"; \
		exit 1; \
	fi
	@chmod +x ./scripts/installations/local-taps-manager.py
	@./scripts/installations/local-taps-manager.py backup "$(DIR)"

local-taps-restore: ## 🏠 Restore local taps (usage: make local-taps-restore DIR=backup-dir)
	@if [ -z "$(DIR)" ]; then \
		echo "Usage: make local-taps-restore DIR=backup-directory"; \
		exit 1; \
	fi
	@chmod +x ./scripts/installations/local-taps-manager.py
	@./scripts/installations/local-taps-manager.py restore "$(DIR)"

##@ DEVELOPMENT & TESTING

build: ## 🐳 Build Neovim test environment
	@docker build --pull . -t neovim

container-bash: ## 🐳 Run bash in testing container
	@docker run -it --rm neovim:latest /bin/bash

show-git-submodule: ## 🔗 Show git submodule status
	@echo "Show submodule list:"
	@git submodule status

##@ INTERNAL STEPS (Installation)

install-step-1-local-taps: ## Step 1/7: Restore local taps
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 1/7: Local Homebrew Taps Restoration\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@$(MAKE) install-local-taps || printf "\033[93m⚠️  Step 1 failed but continuing...\033[0m\n"

install-step-2-packages: ## Step 2/7: Install Homebrew packages
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 2/7: Homebrew Packages Installation\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all || printf "\033[93m⚠️  Step 2 failed but continuing...\033[0m\n"

install-step-3-brew-upgrade: ## Step 3/7: Update all packages to latest versions
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 3/7: Homebrew Packages Update\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🔄 Updating all Homebrew packages to latest versions..."
	@brew upgrade --greedy || printf "\033[93m⚠️  Step 3 failed but continuing...\033[0m\n"
	@echo "🧹 Cleaning up old package versions..."
	@brew cleanup || printf "\033[93m⚠️  Cleanup failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 3 completed\033[0m\n"

install-step-4-git-submodules: ## Step 4/7: Install git submodules
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 4/7: Git Submodules Installation\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@chmod +x ./scripts/installations/git-submodule.py
	@./scripts/installations/git-submodule.py || printf "\033[93m⚠️  Step 4 failed but continuing...\033[0m\n"

install-step-5-dotfiles: ## Step 5/7: Create dotfiles symlinks
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 5/7: Dotfiles Symlinks Creation\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@chmod +x ./scripts/installations/dotfiles.py
	@./scripts/installations/dotfiles.py || printf "\033[93m⚠️  Step 5 failed but continuing...\033[0m\n"

install-step-6-language-managers: ## Step 6/7: Setup language managers
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 6/7: Language Managers Setup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@chmod +x ./scripts/installations/language-managers.py
	@./scripts/installations/language-managers.py || printf "\033[93m⚠️  Step 6 failed but continuing...\033[0m\n"

install-step-7-neovim: ## Step 7/7: Install Neovim plugins
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 7/7: Neovim Plugins Installation\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@chmod +x ./scripts/installations/neovim.py
	@./scripts/installations/neovim.py || printf "\033[93m⚠️  Step 7 failed but continuing...\033[0m\n"

##@ INTERNAL STEPS (Cleanup)

clean-step-1-brew-packages: ## Step 1/7: Remove Homebrew packages
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 1/7: Homebrew Packages Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🍺 Removing all Homebrew formulae and casks..."
	@chmod +x ./scripts/cleanup/brew-packages.py
	@./scripts/cleanup/brew-packages.py -y || printf "\033[93m⚠️  Step 1 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 1 completed\033[0m\n"

clean-step-2-language-managers: ## Step 2/7: Remove language managers
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 2/7: Language Managers Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🔧 Removing Python, Node.js, Java, Rust, Go environments..."
	@chmod +x ./scripts/cleanup/language-managers.py
	@./scripts/cleanup/language-managers.py -y || printf "\033[93m⚠️  Step 2 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 2 completed\033[0m\n"

clean-step-3-neovim: ## Step 3/7: Remove Neovim dynamic content
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 3/7: Neovim Dynamic Content Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "📝 Removing Neovim plugins, cache, and dynamic content..."
	@chmod +x ./scripts/cleanup/neovim.py
	@./scripts/cleanup/neovim.py -y || printf "\033[93m⚠️  Step 3 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 3 completed\033[0m\n"

clean-step-4-dotfiles: ## Step 4/7: Remove dotfiles symlinks
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 4/7: Dotfiles Symlinks Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "⚙️  Removing all dotfiles symlinks..."
	@chmod +x ./scripts/cleanup/dotfiles.py
	@./scripts/cleanup/dotfiles.py -y || printf "\033[93m⚠️  Step 4 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 4 completed\033[0m\n"

clean-step-5-local-taps: ## Step 5/7: Remove local Homebrew taps
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 5/7: Local Homebrew Taps Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🏠 Backing up and removing custom Homebrew taps..."
	@chmod +x ./scripts/cleanup/local-taps.py
	@./scripts/cleanup/local-taps.py -y || printf "\033[93m⚠️  Step 5 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 5 completed\033[0m\n"

clean-step-6-git-submodules: ## Step 6/7: Remove git submodules
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 6/7: Git Submodules Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🔗 Deinitializing and removing git submodules..."
	@chmod +x ./scripts/cleanup/git-submodules.py
	@./scripts/cleanup/git-submodules.py -y || printf "\033[93m⚠️  Step 6 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 6 completed\033[0m\n"

clean-step-7-caches: ## Step 7/7: Remove development caches
	@printf "\033[96m============================================================\033[0m\n"
	@printf "\033[96mStep 7/7: Development Caches Cleanup\033[0m\n"
	@printf "\033[96m============================================================\033[0m\n"
	@echo "🗑️  Removing all development caches..."
	@chmod +x ./scripts/cleanup/caches.py
	@./scripts/cleanup/caches.py -y || printf "\033[93m⚠️  Step 7 failed but continuing...\033[0m\n"
	@printf "\033[92m✅ Step 7 completed\033[0m\n"