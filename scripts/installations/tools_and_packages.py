#!/usr/bin/python3

from __future__ import print_function
import itertools
import os

BREW_TAP_LIST = """
hashicorp/tap
"""

# BREW_LIST_WITH_ARGS = """
# vim --with-lua --with-luajit
# macim --with-lua --with-luajit
# findutils --with-default-names
# gnu-indent --with-default-names
# gnu-sed --with-default-names
# gnu-tar --with-default-names
# gnu-which --with-default-names
# grep --with-default-names
# wdiff --with-gettext
# """

# BREW_LIST = """ brew-cask binutils diffutils gawk gnutls gzip screen watch
# wget zsh unrar cgdb make vim p7zip gnu-time gnu-which gnuplot grep sqlite tig
# doxygen graphviz ctags cscope git gnu-tar tmux screen cmake
# """

BREW_LIST = """
    zsh git tree ag xquartz fzf sshs
    neovim ctags-exuberant
    ansible terraform terragrunt
    kubectl kind minikube helm argocd cog
    nvm go python3 pyenv pipx
    awscli google-cloud-sdk amazon-q
"""

# PIP_PACKAGE_LIST = """cython ipython pylint pep8 pyscope flask nikola markdown nose"""

PIP_PACKAGE_LIST = """
    virtualenv
    poetry
"""

# CABAL_PACKAGE_LIST = """happy pandoc hakyll ghc-mod hlint"""

# SETTING_COMMANDS_INIT = """brew update cabal update"""

PREPARING = """rm -rf ~/.nvm && mkdir ~/.nvm"""
SETTING_COMMANDS_INIT = """brew update"""

# SETTING_COMMANDS_POST = """sudo rm -rf /usr/bin/tar
# sudo ln -s /usr/local/bin/gtar /usr/bin/tar
# sudo rm -rf /usr/bin/ctags
# sudo ln -s /usr/local/bin/ctags /usr/bin/ctags
# brew cask alfred link
# brew linkapps"""


def generateCommandByWords(cmd, words):
    packages = [p for p in words.split() if p]
    return [" ".join([cmd, p]) for p in packages]


def generateCommandByLines(cmd, lines):
    packages = [p for p in lines.splitlines() if p]
    return [" ".join([cmd, " ".join(p.split())]) for p in packages]


def main():
    cmd_seeting = [
        {"cmd": "", "list": PREPARING, "generator": generateCommandByLines},
        {"cmd": "", "list": SETTING_COMMANDS_INIT, "generator": generateCommandByLines},
        {"cmd": "brew tap", "list": BREW_TAP_LIST, "generator": generateCommandByWords},
        {"cmd": "brew install", "list": BREW_LIST, "generator": generateCommandByWords},
        {"cmd": "pipx install", "list": PIP_PACKAGE_LIST, "generator": generateCommandByWords},
        # {"cmd": "brew install", "list": BREW_LIST_WITH_ARGS, "generator": generateCommandByLines},
        # {"cmd": "cabal install", "list": CABAL_PACKAGE_LIST, "generator": generateCommandByWords},
        # {"cmd": "", "list": SETTING_COMMANDS_POST, "generator": generateCommandByLines}
    ]

    cmds = [c['generator'](c['cmd'], c['list']) for c in cmd_seeting]
    cmds = list(itertools.chain(*cmds))

    for cmd in cmds:
        print("Running cmd:", cmd)
        os.system(cmd)
        print("Finish")

if __name__ == '__main__':
    main()
