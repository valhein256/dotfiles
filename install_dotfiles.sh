#!/bin/bash
CURRENT_PATH=`pwd`
OS_PLATFORM=`uname`

info () {
  printf "\r  [ \033[00;34m..\033[0m ] $1\n"
}

user () {
  printf "\r  [ \033[0;33m?\033[0m ] $1 "
}

success () {
  printf "\r\033[2K  [ \033[00;32mOK\033[0m ] $1\n"
}

fail () {
  printf "\r\033[2K  [\033[0;31mFAIL\033[0m] $1\n"
  echo ""
  exit
}

install_dotfiles () {
  echo "### dotfiles setting... "
  ### link dotfiles files ###
  ln -s $CURRENT_PATH/gitconfig           $HOME/.gitconfig
  ln -s $CURRENT_PATH/screenrc            $HOME/.screenrc
  if [[ ! -d $HOME/.ssh ]]; then
        mkdir -p $HOME/.ssh
  fi
  ln -s $CURRENT_PATH/sshrc               $HOME/.ssh/rc
  ### end ###

  ### link zsh files ###
  if [[ ! -d $HOME/.zplug ]]; then
    ln -s $CURRENT_PATH/zsh/zplug $HOME/.zplug
  fi
  ln -s $CURRENT_PATH/zsh/zshrc             $HOME/.zshrc       
  ### end ###

  # install tmux plugin manager
  if [[ ! -d $HOME/.tmux ]]; then
    ln -s $CURRENT_PATH/tmux $HOME/.tmux
  fi
  ln -s $HOME/.tmux/tmux.conf             $HOME/.tmux.conf
  ### end ###

  echo -e "\033[32m### Finish !!\033[0m"
  echo ""
}

install_vim_plug () {
  echo "### vim setting... "
  # install vim plugin manager
  if [[ ! -d $HOME/.vim ]]; then
    ln -s $CURRENT_PATH/vim $HOME/.vim
  fi
  ln -s $HOME/.vim/vimrc             $HOME/.vimrc
  ### end ###
  echo -e "\033[32m### Finish !!\033[0m"
  echo ""
  
  echo "### vim-plug installing... "
  # download plug.vim
  curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

  # Install vim plugins
  vim -es -u $CURRENT_PATH/vim/vimrc -i NONE -c "PlugInstall" -c "qa"
  echo -e "\033[32m### Finish !!\033[0m"
  echo ""
}

############################
# Start installation
############################

echo ""
echo -e "### Git submodule init & update"
if [[ ! -f $CURRENT_PATH/.gitmodules ]]; then
  ./scripts/git_submodule_add.sh
fi
git submodule init
git submodule update --recursive
./scripts/git_submodule_update.sh
echo -e "\033[32m### Finish !!\033[0m"
echo ""

echo -e "### Installing..."
install_dotfiles 
#install_vim_plug
cd ./neovim && ./install_darwin.sh
echo -e "\033[32m### All installed!\033[0m"
echo ""

