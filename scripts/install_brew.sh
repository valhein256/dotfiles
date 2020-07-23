#!/bin/bash -e

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

install_homebrew () {
  echo "### Homebrew installing... "
  if test ! $(which brew)
  then
    echo "### Installing Homebrew for you... "
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  fi
  echo -e "\033[32m### Finish !!\033[0m"
  echo ""
}

install_homebrew
