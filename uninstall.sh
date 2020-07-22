#!/bin/bash

CLEANRC=all

help() {
  cat << EOF
usage: $0 [OPTIONS]
    -c      Clean dotfilers rc

    example:
        ./uninstall_dotfiles.sh or ./uninstall_dotfiles.sh -c all
        ./uninstall_dotfiles.sh -c zsh
        ./uninstall_dotfiles.sh -c vim
        ./uninstall_dotfiles.sh -c other
        ./uninstall_dotfiles.sh -c all
EOF
}

cleanZshrc (){
    FILES=(
        $HOME/.zshrc       
    )
    tLen=${#FILES[@]}

    for (( i=0; i<${tLen}; i++ ));
    do
      if [[ -e ${FILES[$i]} ]]; then
          echo "rm -rf ${FILES[$i]}"
          rm -rf ${FILES[$i]}
      else
          echo "${FILES[$i]} doesn't exist"
      fi
    done
}

cleanVimrc (){
    FILES=(
        $HOME/.vimrc
        $HOME/.vim
    )
    tLen=${#FILES[@]}

    for (( i=0; i<${tLen}; i++ ));
    do
      if [[ -e ${FILES[$i]} ]]; then
          echo "rm -rf ${FILES[$i]}"
          rm -rf ${FILES[$i]}
      else
          echo "${FILES[$i]} doesn't exist"
      fi
    done
}

cleanOther (){
    FILES=(
        $HOME/.gitconfig
        $HOME/.tmux.conf
        $HOME/.screenrc
        $HOME/.ssh/rc
        $HOME/.tmux
        $HOME/.zplug
    )
    tLen=${#FILES[@]}

    for (( i=0; i<${tLen}; i++ ));
    do
      if [[ -e ${FILES[$i]} ]]; then
          echo "rm -rf ${FILES[$i]}"
          rm -rf ${FILES[$i]}
      else
          echo "${FILES[$i]} doesn't exist"
      fi
    done
}

while getopts c:h opt
do
    case $opt in
        c)  CLEANRC=$OPTARG;;
        h)  help
            exit 0
            ;;
        \?) echo "Invalid option -$OPTARG" >&2;;
    esac
done

# remove the previous files

if [ "$CLEANRC" == zsh ]; then
    cleanZshrc
elif [ "$CLEANRC" == vim ]; then
    cleanVimrc
elif [ "$CLEANRC" == other ]; then
    cleanOther
elif [ "$CLEANRC" == all ]; then
    cleanZshrc
    cleanVimrc
    cleanOther
fi

