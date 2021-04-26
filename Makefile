build:
	@docker build --pull . -t neovim

launch:
	@docker run -it --rm neovim:latest /bin/bash

reinstall_all: clean install_all

install_all:
	@./scripts/installations/git-submodule.sh
	@./scripts/installations/dotfiles.sh
	@./scripts/installations/neovim.sh

clean:
	@-rm -rf ./neovim/plugged/ | true
	@-rm -rf ./neovim/autoload/ | true
	@-rm -rf ./neovim/env/ | true
	@-find ./zsh/zplug -delete | true
	@-find ./tmux/plugins/tpm -delete |true
	@./scripts/remove_dotfiles.sh

show:
	@echo "Show submodule list:"
	@git submodule status
	@echo	
	@echo "Show Makefile command:"
	@cat Makefile

test_install_nvim:
	@./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim:
	@./scripts/uninstall_nvim_ubuntu.sh
