#!/bin/bash

CLEANRC=all

help() {
  cat << EOF
usage: $0 [OPTIONS]
    -c      Clean dotfilers rc

    example:
        ./remove_dotfiles.sh or ./remove_dotfiles.sh -c all
        ./remove_dotfiles.sh -c zsh
        ./remove_dotfiles.sh -c vim
        ./remove_dotfiles.sh -c other
        ./remove_dotfiles.sh -c all
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

cleanNeovimrc (){
    FILES=(
        $HOME/.config/nvim
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

cleanTools (){
    FILES=(
        $HOME/.tools
    )
    tLen=${#FILES[@]}

    for (( i=0; i<${tLen}; i++ ));
    do
      if [[ -e ${FILES[$i]} || -L ${FILES[$i]} ]]; then
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
      if [[ -e ${FILES[$i]} || -L ${FILES[$i]} ]]; then
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
    cleanNeovimrc
    cleanOther
fi

