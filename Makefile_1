pull_ubuntu_image:
	docker pull ubuntu

launch_env:
	docker run -it  \
		-v `pwd`:/usr/dotfiles \
		ubuntu:latest /bin/bash

install_all:
	./scripts/install_dotfiles.sh
	./scripts/install_nvim.sh

uninstall_all:
	./scripts/uninstall.sh

test_install_nvim:
	./scripts/install_nvim_ubuntu.sh

test_uninstall_nvim:
	./scripts/uninstall_nvim_ubuntu.sh
