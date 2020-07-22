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


echo -e "### Homebrew installing..."
install_homebrew
echo -e "\033[32m### Homebrew installed!\033[0m"
echo ""
echo -e "### Packages installing..."
brew install neovim python3 python3-pip python3-venv exuberant-ctags
brew install ag
echo -e "\033[32m### !\033[0m"
echo ""
