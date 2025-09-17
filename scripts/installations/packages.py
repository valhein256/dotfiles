#!/usr/bin/python3

from __future__ import print_function
import itertools
import os

BREW_TAP_LIST = """
hashicorp/tap
"""

BREW_LIST = """
    zsh git tree ag xquartz fzf sshs
    neovim ctags-exuberant
    ansible terraform terragrunt
    kubectl kind minikube helm argocd cog
    nvm go python3 pyenv pipx
    awscli google-cloud-sdk amazon-q
"""

PIP_PACKAGE_LIST = """
    virtualenv
    poetry
"""

NPM_PACKAGE_LIST = """
    aws-cdk
"""

PREPARING = """rm -rf ~/.nvm && mkdir ~/.nvm"""
SETTING_COMMANDS_INIT = """brew update"""

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
        {"cmd": "npm install -g", "list": NPM_PACKAGE_LIST, "generator": generateCommandByWords},
    ]

    cmds = [c['generator'](c['cmd'], c['list']) for c in cmd_seeting]
    cmds = list(itertools.chain(*cmds))

    for cmd in cmds:
        print("Running cmd:", cmd)
        os.system(cmd)
        print("Finish")

if __name__ == '__main__':
    main()
