build:
	docker build --pull . -t neovim

launch:
	docker run -it --rm \
		neovim:latest /bin/bash

install_all:
	./scripts/install_dotfiles.sh
	./scripts/install_nvim.sh

uninstall_all:
	./scripts/uninstall.sh

test_install_nvim:
	./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim:
	./scripts/uninstall_nvim_ubuntu.sh
