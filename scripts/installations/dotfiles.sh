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
echo -e "\033[90m#####################################\033[0m"
echo -e "\033[90m# scripts/installations/dotfiles.sh #\033[0m"
echo -e "\033[90m#####################################\033[0m"
echo ""
echo -e "### Dotfiles setting..."
### link dotfiles files ###
echo -e "gitconfig setting..."
if [[ -e $HOME/.gitconfig ]]; then
    rm -rf $HOME/.gitconfig
fi
ln -s $CURRENT_PATH/gitconfig           $HOME/.gitconfig
echo -e "gitconfig setting... done !!"

echo -e "screenrc setting..."
if [[ -e $HOME/.screenrc ]]; then
    rm -rf $HOME/.screenrc
fi
ln -s $CURRENT_PATH/screenrc            $HOME/.screenrc
echo -e "screenrc setting... done !!"

echo -e "sshrc setting..."
if [[ ! -d $HOME/.ssh ]]; then
      mkdir -p $HOME/.ssh
fi
if [[ -e $HOME/.ssh/rc ]]; then
    rm -rf $HOME/.ssh/rc
fi
ln -s $CURRENT_PATH/sshrc               $HOME/.ssh/rc
echo -e "sshrc setting... done !!"
### end ###

### link zsh files ###
echo -e "zsh files setting..."
if [[ ! -d $HOME/.zplug ]]; then
  ln -s $CURRENT_PATH/zsh/zplug $HOME/.zplug
fi
if [[ -e $HOME/.zshrc ]]; then
    rm -rf $HOME/.zshrc
fi
ln -s $CURRENT_PATH/zsh/zshrc           $HOME/.zshrc
echo -e "zsh files setting... done !!"
### end ###

# install tmux plugin manager
echo -e "tmux setting..."
if [[ ! -d $HOME/.tmux ]]; then
  ln -s $CURRENT_PATH/tmux $HOME/.tmux
fi
if [[ -e $HOME/.tmux.conf ]]; then
    rm -rf $HOME/.tmux.conf
fi
ln -s $HOME/.tmux/tmux.conf             $HOME/.tmux.conf
echo -e "tmux setting... done !!"
echo -e "### Dotfiles setting... done !!"
### end ###

### link tools files ###
echo -e "tools files setting..."
if [[ ! -d $HOME/.tools ]]; then
  ln -s $CURRENT_PATH/tools $HOME/.tools
fi
### end ###

echo ""
echo -e "\033[32m# scripts/installations/dotfiles.sh Finish !!\033[0m"
echo ""
