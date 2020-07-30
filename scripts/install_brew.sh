#!/bin/bash -e


# ==> This script will install:
# /usr/local/bin/brew
# /usr/local/share/doc/homebrew
# /usr/local/share/man/man1/brew.1
# /usr/local/share/zsh/site-functions/_brew
# /usr/local/etc/bash_completion.d/brew
# /usr/local/Homebrew
# ==> The following existing directories will be made group writable:
# /usr/local/lib
# ==> The following existing directories will have their owner set to wu-hsuan_lin:
# /usr/local/lib
# ==> The following existing directories will have their group set to admin:
# /usr/local/lib
# ==> The following new directories will be created:
# /usr/local/bin
# /usr/local/etc
# /usr/local/include
# /usr/local/sbin
# /usr/local/share
# /usr/local/var
# /usr/local/opt
# /usr/local/share/zsh
# /usr/local/share/zsh/site-functions
# /usr/local/var/homebrew
# /usr/local/var/homebrew/linked
# /usr/local/Cellar
# /usr/local/Caskroom
# /usr/local/Homebrew
# /usr/local/Frameworks


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
