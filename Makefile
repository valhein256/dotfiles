build:
	docker build --pull . -t neovim

launch:
	docker run -it --rm neovim:latest /bin/bash

install_all:
	./scripts/installations/git-submodules.sh
	./scripts/installations/dotfiles.sh
	./scripts/installations/neovim.sh

uninstall_all:
	./scripts/uninstall.sh

show:
	@echo "Show submodule list:"
	@git submodule status
	@echo	
	@echo "Show Makefile command:"
	@cat Makefile

test_install_nvim:
	./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim:
	./scripts/uninstall_nvim_ubuntu.sh
