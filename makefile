pull_ubuntu_image:
	docker pull ubuntu

launch_env:
	# Here we also mount /plu for runtime dependency
	docker run -it  \
		-v `pwd`:/usr/dotfiles \
		ubuntu:latest /bin/bash

