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
echo -e "### Git submodule init & update..."
if [[ ! -f $CURRENT_PATH/.gitmodules ]]; then
  # zplug
  git submodule add https://github.com/zplug/zplug zsh/zplug
  # tmux plugin: tpm
  git submodule add https://github.com/tmux-plugins/tpm tmux/plugins/tpm
fi
git submodule init
git submodule update --recursive
git submodule foreach --recursive git pull origin master
echo -e "\033[32m### Finish !!\033[0m"
echo ""
