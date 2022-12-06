
##@ Helpers

.PHONY: help

help: ## Display this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST) && echo

##@ OPERATION

reinstall: clean install-libs ## Reinstall

install-libs: ## Install
	@./scripts/installations/git-submodule.sh
	@./scripts/installations/dotfiles.sh
	@./scripts/installations/neovim.sh

install-package: ## Install packages
	@./scripts/packages.py

clean: ## Clean
	@-rm -rf ./neovim/plugged/ | true
	@-rm -rf ./neovim/autoload/ | true
	@-rm -rf ./neovim/env/ | true
	@-find ./zsh/zplug -delete | true
	@-find ./tmux/plugins/tpm -delete |true
	@./scripts/remove_dotfiles.sh

show: ## Show submodule list
	@echo "Show submodule list:"
	@git submodule status

##@ TESTING

build: ## build neovim tset environment 
	@docker build --pull . -t neovim

container-bash: ## Run bash in testing container
	@docker run -it --rm neovim:latest /bin/bash

test_install_nvim: ## Test scripts/install_nvim_ubuntu.sh in container-bash
	@./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim: ## Test ./scripts/uninstall_nvim_ubuntu.sh in container-bash
	@./scripts/uninstall_nvim_ubuntu.sh
