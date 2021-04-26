#!/bin/bash -e

CURRENT_PATH=`pwd`

# Make config directory for Neovim's init.vim
echo '[*] Preparing Neovim config directory ...'
mkdir -p $HOME/.config/
if [[ ! -f $HOME/.config/nvim ]]; then
  ln -sfn $CURRENT_PATH/neovim $HOME/.config/nvim
fi

# Install virtualenv to containerize dependencies
echo '[*] Pip installing venv to containerize Neovim dependencies (instead of installing them onto your system) ...'
python3 -m venv $HOME/.config/nvim/env

# Install pip modules for Neovim within the virtual environment created
echo '[*] Activating virtualenv and pip installing Neovim (for Python plugin support), libraries for async autocompletion support (jedi, psutil, setproctitle), and library for pep8-style formatting (yapf) ...'
source $HOME/.config/nvim/env/bin/activate
pip install wheel
pip install pynvim jedi psutil setproctitle yapf doq # run `pip uninstall neovim pynvim` if still using old neovim module
deactivate

# Install vim-plug plugin manager
echo '[*] Downloading vim-plug, the best minimalistic vim plugin manager ...'
curl -fLo $HOME/.config/nvim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Enter Neovim and install plugins using a temporary init.vim, which avoids warnings about missing colorschemes, functions, etc
echo -e '[*] Running :PlugInstall within nvim ...'
nvim -c ':PlugInstall' -c ':UpdateRemotePlugins' -c ':qall'

echo -e "[+] Done, welcome to \033[1m\033[92mNeoVim\033[0m! Try it by running: nvim/vim. Want to customize it? Modify $HOME/.config/nvim/init.vim"

