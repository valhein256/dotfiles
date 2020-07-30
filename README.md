# Pre-processing
    * Install docker
    * Install powerline fonts: https://github.com/powerline/fonts
    * Run ./install_brew.sh & ./install_brew_packages.py
    * Make sure you have pip3.
    * Run ./install_dotfiles.sh

# Install steps:

# Init git submodule
    * $ ./scripts/git_submodule_add.sh
    * git submodule add https://github.com/zplug/zplug zsh/zplug
    * git submodule add https://github.com/tmux-plugins/tpm tmux/plugins/tpm

# Git config setting
    * set global:
      * git config --global user.name ""
      * git config --global user.email ""

    * set local:
      * git config --local user.name ""
      * git config --local user.email ""

# Vim setting
Ref: 
    1. https://blog.m157q.tw/posts/2018/07/23/use-my-old-vimrc-for-neovim/
   
# Error case
Ref:
    1. https://blog.csdn.net/qq_42672770/article/details/87182133
    2. https://stackoverflow.com/questions/13762280/zsh-compinit-insecure-directories/41674919#41674919
     
# Todo
    1. The installation steps of theme and font
      a. https://github.com/ryanoasis/nerd-fonts#option-1-download-and-install-manually 
      b. https://github.com/mbadolato/iTerm2-Color-Schemes
