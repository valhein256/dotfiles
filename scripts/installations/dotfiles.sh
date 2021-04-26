#!/bin/bash -e
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

############################
# Start installation
############################

echo ""
echo -e "### Dotfiles setting..."
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
ln -s $CURRENT_PATH/zsh/zshrc           $HOME/.zshrc
### end ###

# install tmux plugin manager
if [[ ! -d $HOME/.tmux ]]; then
  ln -s $CURRENT_PATH/tmux $HOME/.tmux
fi
ln -s $HOME/.tmux/tmux.conf             $HOME/.tmux.conf
### end ###

echo -e "\033[32m### Finish !!\033[0m"
echo ""
