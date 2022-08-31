# MacOS Setup Guide
Ref: 
* https://sourabhbajaj.com/mac-setup/
* https://project-awesome.org/unixorn/awesome-zsh-plugins

## Installation
### Application
Go to the website to install these applications directly
* Browser: [Chrome], [FireFox]
* [Docker]
* [VirtualBox]
* [Vagrant]
* [iTerm2]

### Dotfiles
#### Add SSH Key to Gitlab Account
To add an SSH key you need to generate one or use an existing key.
```sh
$ ssh-keygen -t rsa -b 2048 -C "email@example.com"
$ cat ~/.ssh/id_rsa.pub
```
Paste the content of catting to [Gitlab profile keys]
#### Clone / Download
If the system has git command, use git clone to fetch dotfiles repos.
```sh
$ git clone git@gitlab.com:valhein256/dotfiles.git
```
Or you could download the repos from gitlab.

#### Homebrew
Go to [Homebrew], and install it.
After install howebrew, run the scripts: scripts/packages.py to install required packages.
```sh
$ cd /path/to/dotfiles
$ ./scripts/packages.py
```
Package list:
* Brew
    * neovim 
    * python3 
    * ctags-exuberant 
    * ag 
    * zsh 
    * git 
    * node 
    * awscli 
    * tree 
    * go
* Python Packages
    * virtualenv

##### Error case
If you encountered following problem when the script:./scripts/packages.py was running
```sh
Error: The following directories are not writable by your user:
/usr/local/share/zsh
/usr/local/share/zsh/site-functions

You should change the ownership of these directories to your user.
sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions
```
#### Dotfiles and Neovim-config
After install howebrew and packages, run make command to install Dotfiles and Neovim-config.
```sh
$ cd /path/to/dotfiles
$ make install_all
```
#### Font and Theme
##### Font
Ref: https://github.com/Homebrew/homebrew-cask-fonts
```sh
$ brew tap homebrew/cask-fonts && brew install font-sauce-code-pro-nerd-font # Install Source Code Pro With Nerd Font.
```
After install Source Code Pro With Nerd Font...
Go to iTerm2 preferences -> Profiles -> Text -> Select the font: SauceCodePro Nerd Font.
##### Theme
Go to [iterm2-color-schemes] to download the resources.
After unzip the resources...
Go to iTerm2 preferences -> Profiles -> Colors -> Select the colors: Hurtado.
##### Ref
* https://github.com/mbadolato/iTerm2-Color-Schemes
* https://iterm2colorschemes.com/
* https://github.com/ryanoasis/nerd-fonts#option-1-download-and-install-manually
* https://github.com/Homebrew/homebrew-cask-fonts
* https://github.com/ryanoasis/nerd-fonts/tree/master/patched-fonts/SourceCodePro
#### Dotfiles and Neovim Installing and Setup
```sh
$ cd /path/to/dotfiles
$ make install_all
```
After the installation is finished, restart the zsh to install the zsh-plugins.
##### Error case
If you encountered following problem when launch a new zsh after installing... 
```sh
zsh compinit: insecure directories, run compaudit for list.
Ignore insecure directories and continue [y] or abort compinit [n]? 

You should change the ownership of these directories to your user.
sudo chmod 755 /usr/local/share/zsh /usr/local/share/zsh/site-functions 
sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions
```
### Git Config Setting
#### Global
```sh
$ git config --global user.name "..."
$ git config --global user.email "..."
```
#### Local
```sh
$ git config --local user.name "..."
$ git config --local user.email "..."
```
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
   [Gitlab profile keys]: <https://gitlab.com/-/profile/keys>

