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
	@echo "  � Patckage Updates - Update all installed packages to latest versions"
	@echo "  🔗 Git Submodules - Initialize zplug and tmux plugins"
	@echo "  ⚙️  Dotfiles - Create symlinks for all configuration files"
	@echo "  �  Language Managers - Setup Python, Node.js, Java, Rust, Go"
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
	if [ "$$confirm" != "INSTALL" ]; then \
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
	@printf "\033[91m# 🧹 COMPLETE SYSTEM CLEANUP �         #\033[0m\n"
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
	if [ "$$confirm" != "CLEANUP" ]; then \
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
	@echo "    � Updatae all packages to latest versions"
	@echo "    🔗 Initialize git submodules"
	@echo "    ⚙️  Create dotfiles symlinks"
	@echo "    � ISetup language managers"
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
	if [ "$$confirm" != "RESET" ]; then \
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

system-status: ## 📊 Check comprehensive system status (usage: make system-status CHECK_TYPE=cleaned|installed)
	@chmod +x ./scripts/verifications/system-status-checker.py
	@if [ -z "$(CHECK_TYPE)" ]; then \
		echo "📊 System Status Check"; \
		echo "CHECK_TYPE: default (installation status)"; \
		echo ""; \
		./scripts/verifications/system-status-checker.py; \
	else \
		echo "📊 System Status Check"; \
		echo "CHECK_TYPE: $(CHECK_TYPE)"; \
		echo ""; \
		./scripts/verifications/system-status-checker.py --check-type $(CHECK_TYPE); \
	fi

system-status-cleaned: ## 📊 Check system cleanup status (verify removal)
	@echo "📊 System Status Check"
	@echo "CHECK_TYPE: cleaned"
	@echo ""
	@chmod +x ./scripts/verifications/system-status-checker.py
	@./scripts/verifications/system-status-checker.py --check-type cleaned

system-status-installed: ## 📊 Check system installation status (verify installation)
	@echo "📊 System Status Check"
	@echo "CHECK_TYPE: installed"
	@echo ""
	@chmod +x ./scripts/verifications/system-status-checker.py
	@./scripts/verifications/system-status-checker.py --check-type installed

install-verify: ## ✅ Verify installation completeness
	@chmod +x ./scripts/verifications/installation-verification.py
	@./scripts/verifications/installation-verification.py

cleanup-verify: ## ✅ Verify cleanup completeness
	@chmod +x ./scripts/verifications/cleanup-verification.py
	@./scripts/verifications/cleanup-verification.py

system-status-sequential: ## 📊 Check system status (sequential mode, usage: CHECK_TYPE=cleaned|installed)
	@chmod +x ./scripts/verifications/system-status-checker.py
	@if [ -z "$(CHECK_TYPE)" ]; then \
		./scripts/verifications/system-status-checker.py --sequential; \
	else \
		./scripts/verifications/system-status-checker.py --sequential --check-type $(CHECK_TYPE); \
	fi

system-status-packages: ## 📦 Check only package status (usage: CHECK_TYPE=cleaned|installed)
	@chmod +x ./scripts/verifications/system-status-checker.py
	@if [ -z "$(CHECK_TYPE)" ]; then \
		./scripts/verifications/system-status-checker.py --packages-only; \
	else \
		./scripts/verifications/system-status-checker.py --packages-only --check-type $(CHECK_TYPE); \
	fi

system-status-cleanup: ## 🧹 Check only cleanup status (usage: CHECK_TYPE=cleaned|installed)
	@chmod +x ./scripts/verifications/system-status-checker.py
	@if [ -z "$(CHECK_TYPE)" ]; then \
		./scripts/verifications/system-status-checker.py --cleanup-only; \
	else \
		./scripts/verifications/system-status-checker.py --cleanup-only --check-type $(CHECK_TYPE); \
	fi

##@ COMPONENT INSTALLATION

install-packages: ## 📦 Install Homebrew packages only
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all

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

brew-install-formula: ## 🍺 Install from formula file (usage: make brew-install-formula FORMULA=formulas/tool.rb)
	@if [ -z "$(FORMULA)" ]; then \
		echo "Usage: make brew-install-formula FORMULA=path/to/formula.rb"; \
		exit 1; \
	fi
	@chmod +x ./scripts/installations/brew-manager.py
	@./scripts/installations/brew-manager.py install-formula "$(FORMULA)"

brew-clean-taps: ## 🚰 Remove custom Homebrew taps (hashicorp/tap, etc.)
	@echo "🚰 Removing custom Homebrew taps..."
	@python3 -c "\
import subprocess; \
result = subprocess.run('brew tap', shell=True, capture_output=True, text=True); \
custom_taps = [tap.strip() for tap in result.stdout.split('\n') if tap.strip() and not tap.startswith('homebrew/')]; \
print(f'Found {len(custom_taps)} custom taps: {custom_taps}') if custom_taps else print('No custom taps found'); \
[subprocess.run(f'brew untap {tap}', shell=True) for tap in custom_taps]; \
print('✅ Custom taps removed') if custom_taps else None"

brew-list-formulas: ## 🍺 List available custom formulas
	@chmod +x ./scripts/installations/brew-manager.py
	@./scripts/installations/brew-manager.py list-formulas

brew-update: ## 🍺 Update Homebrew and packages
	@chmod +x ./scripts/installations/brew-manager.py
	@./scripts/installations/brew-manager.py update

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

local-taps-validate: ## 🏠 Validate all local taps
	@chmod +x ./scripts/installations/local-taps-manager.py
	@./scripts/installations/local-taps-manager.py validate

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
	@$(MAKE) restore-local-taps || printf "\033[93m⚠️  Step 1 failed but continuing...\033[0m\n"

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

##@ LEGACY COMPATIBILITY

packages: ## 📦 Legacy: Install all packages
	@echo "Install all packages..."
	@chmod +x ./scripts/installations/packages.py
	@./scripts/installations/packages.py install --all
	@echo "Done"

language-managers: ## 🔧 Legacy: Setup language managers
	@echo "Setup language version managers..."
	@chmod +x ./scripts/installations/language-managers.py
	@./scripts/installations/language-managers.py
	@echo "Done"

git-submodule: ## 🔗 Legacy: Install git submodules
	@echo "Install git-submodule..."
	@chmod +x ./scripts/installations/git-submodule.py
	@./scripts/installations/git-submodule.py
	@echo "Done"

dotfiles: ## ⚙️ Legacy: Install dotfiles
	@echo "Install dotfiles..."
	@chmod +x ./scripts/installations/dotfiles.py
	@./scripts/installations/dotfiles.py
	@echo "Done"

neovim-plugins: ## 📝 Legacy: Install neovim plugins
	@echo "Install neovim plugins and configurations..."
	@chmod +x ./scripts/installations/neovim.py
	@./scripts/installations/neovim.py
	@echo "Done"

restore-local-taps: ## 🏠 Legacy: Restore local taps
	@echo "Restore local Homebrew taps..."
	@chmod +x ./scripts/installations/local-taps-manager.py
	@if [ -d "./backups/local-taps" ]; then \
		./scripts/installations/local-taps-manager.py restore ./backups/local-taps; \
	else \
		echo "No local taps backup found, skipping..."; \
	fi
	@echo "Done"

post-install-verify: ## ✅ Legacy: Post-install verification
	@chmod +x ./scripts/verifications/post-install-verification.py
	@./scripts/verifications/post-install-verification.py

system-status-workers: ## 📊 Legacy: System status with workers
	@chmod +x ./scripts/verifications/system-status-checker.py
	@if [ -z "$(WORKERS)" ]; then \
		echo "Usage: make system-status-workers WORKERS=number"; \
		echo "Example: make system-status-workers WORKERS=8"; \
		exit 1; \
	fi
	@./scripts/verifications/system-status-checker.py --workers $(WORKERS)