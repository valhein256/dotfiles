# MacOS Setup Guide
References: 
* https://sourabhbajaj.com/mac-setup/
* https://project-awesome.org/unixorn/awesome-zsh-plugins

## Applications Setup Guide

Install the following applications:

* [logi options+] - Logitech Options+ is a powerful and easy-to-use application that enhances your Logic MX Master 3.
* [Chrome]
* [Docker]
* [iTerm2]
* [Homebrew]

Hint: To uninstall logi options+, you can use the following command:

    $ sudo rm -rf /Applications/logioptionsplus.app

## Development Environment Setup Guide

### Prepare

#### Install Xcode Command Line Tools

    $ xcode-select --install

#### Setup Github Account SSH Key

Go to [Github profile keys] to add SSH Key. You can use the following command to generate SSH Key.

    $ ssh-keygen -t rsa -b 2048 -C "email@example.com"
    $ cat ~/.ssh/id_rsa.pub

Paste the content of catting to [Github profile keys]

#### Clone or Download Dotfiles Repos

If the system has git command, use git clone to fetch dotfiles repos.

    $ git clone git@github.com:valhein256/dotfiles.git

Or you can download the repos from github.

### First Time to Install Everythings

For the first time to install everything, you need to install the tools and packages, dotfiles and neovim-config manually in order for the following steps.

#### Tools and Packages

First, to cd to the dotfiles repos.

    $ cd /path/to/dotfiles

Run the scripts: scripts/packages.py to install required packages.

    $ make tools_and_packages

or you can install the packages manually:

    $ ./scripts/installations/tools_and_packages.py

##### Error case

If you encountered following problem when you install tools and packages via make command or scripts

    Error: The following directories are not writable by your user:
    /usr/local/share/zsh
    /usr/local/share/zsh/site-functions

    You should change the ownership of these directories to your user.
    sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions

#### Dotfiles and Neovim-config

After install tools and packages, run make command to install Dotfiles and Neovim-config.

    $ make git-submodule
    $ make dotfiles
    $ make neovim-config

### Reinstall or Update

If you want to reinstall or update the all of the tools, packages, dotfiles and neovim-config, you can use the following commands:

    $ make reinstall

## Others

### Font and Theme Setting

#### Font

To install the font: SauceCodePro Nerd Font, you can use the following commands:

    $ brew install font-sauce-code-pro-nerd-font

After install Source Code Pro With Nerd Font...

Go to iTerm2 Settings -> Profiles -> Text -> Select the font: SauceCodePro Nerd Font.

#### Theme

Go to [iterm2-color-schemes] to download the resources: .tar.gz file or .zip file.

After unzip the resources..., you can import the theme to iTerm2.

Import path: iTerm2 Settings -> Profiles -> Colors -> Color Presets... -> Import..., then select the theme file: ./schemas/Hurtado.itermcolors

Go to iTerm2 Settings -> Profiles -> Colors -> Select the colors: Hurtado.

Hint: The file path may be difference, you may need to find the .itermcolors file in the resources.

Reference:
* https://github.com/Homebrew/homebrew-cask-fonts
* https://github.com/mbadolato/iTerm2-Color-Schemes
* https://iterm2colorschemes.com/
* https://github.com/ryanoasis/nerd-fonts#option-1-download-and-install-manually
* https://github.com/Homebrew/homebrew-cask-fonts
* https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/SourceCodePro

### Git Config Setting

#### Global

    $ git config --global user.name "..."
    $ git config --global user.email "..."

#### Local

    $ git config --local user.name "..."
    $ git config --local user.email "..."

## Troubleshooting

After installation, you might occasionally notice the presence of numerous numbered empty folders within the tmux or zsh directories. 

To address this issue, you can attempt to rerun the installation command. Should these empty folders persist, continue with repeated reinstallations until they no longer appear. 

Commands:

    # Reinstall Command
    $ make reinstall
    # zsh checking
    $ tree -L 2 zsh
    # tmux checking
    $ tree -L 3 tmux

---------

### Other Documents
[What is the difference between venv, pyvenv, pyenv, virtualenv, virtualenvwrapper, pipenv, etc?]

   [Chrome]: <https://www.google.com/chrome/?brand=CHBD&gclid=CjwKCAjw34n5BRA9EiwA2u9k30fBEMblRcv82Os1vwt6z4tOarneYbf-eOGCF4Uy7kVNs4MxcmpE6xoC4lUQAvD_BwE&gclsrc=aw.ds>
   [Firefox]: <https://www.mozilla.org/en-US/>
   [Docker]: <https://www.docker.com/>
   [virtualbox]: <https://www.virtualbox.org/>
   [vagrant]: <https://www.vagrantup.com/>
   [iTerm2]: <https://www.iterm2.com/>
   [Homebrew]: <https://brew.sh/>
   [iterm2-color-schemes]: <https://iterm2colorschemes.com/>
   [Use my old vimrc for NeoVim]: <https://blog.m157q.tw/posts/2018/07/23/use-my-old-vimrc-for-neovim/>
   [What is the difference between venv, pyvenv, pyenv, virtualenv, virtualenvwrapper, pipenv, etc?]: <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe/41573588#41573588>
   [Use my old vimrc for NeoVim]: <https://blog.m157q.tw/posts/2018/07/23/use-my-old-vimrc-for-neovim/>
   [Github profile keys]: <https://github.com/settings/keys>
   [logi options+]: <https://www.logitech.com/en-us/product/options-plus>
