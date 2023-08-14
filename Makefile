##@ Helpers

.PHONY: help

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) && echo

##@ OPERATION

install: tools-and-packages git-submodule dotfiles neovim-plugins ## Install all

reinstall: clean install ## Reinstall all

##@ TOOLS AND PACKAGES

tools-and-packages: ## Step.1 - Install tools and packages
	@echo "Install tools and packages..."
	@./scripts/installations/tools_and_packages.py
	@echo "Done"

##@ DOTFILES AND NEOVIM

git-submodule: ## Step.2 - Install git-submodule
	@echo "Install git-submodule..."
	@./scripts/installations/git-submodule.sh
	@echo "Done"

dotfiles: ## Step.3 - Install dotfiles
	@echo "Install dotfiles..."
	@./scripts/installations/dotfiles.sh
	@echo "Done"

neovim-plugins: ## Step.4 - Install neovim plugins and configurations
	@echo "Install neovim plugins and configurations..."
	@./scripts/installations/neovim.sh
	@echo "Done"

clean: ## Clean all dotfiles and neovim plugins and configurations
	@echo "Clean all dotfiles and neovim plugins and configurations..."
	@rm -rf ./neovim/plugged/ | true
	@rm -rf ./neovim/autoload/ | true
	@rm -rf ./neovim/env/ | true
	@./scripts/remove_dotfiles.sh
	@echo "Done"

show-git-submodule: ## Show submodule list
	@echo "Show submodule list:"
	@git submodule status

##@ NEOVIM TESTING

build: ## build neovim tset environment 
	@docker build --pull . -t neovim

container-bash: ## Run bash in testing container
	@docker run -it --rm neovim:latest /bin/bash

test_install_nvim: ## Test scripts/install_nvim_ubuntu.sh in container-bash
	@./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim: ## Test ./scripts/uninstall_nvim_ubuntu.sh in container-bash
	@./scripts/uninstall_nvim_ubuntu.sh
