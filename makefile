pull_ubuntu_image:
	docker pull ubuntu

launch_env:
	# Here we also mount /plu for runtime dependency
	docker run -it  \
		-v `pwd`:/usr/dotfiles \
		ubuntu:latest /bin/bash

install_all:
	./scripts/install_dotfiles.sh
	cd ./neovim && ./install_darwin.sh

uninstall_all:
	./scripts/uninstall.sh
