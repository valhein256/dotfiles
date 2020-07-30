# MacOS Setup Guide
Ref: https://sourabhbajaj.com/mac-setup/

### Application 
* Browser: [Chrome], [FirFox]
* [Docker]
* [VirtualBox]
* [Vagrant]
* [iTerm2]
### Dotfiles
#### Add an SSH key
To add an SSH key you need to generate one or use an existing key.
```sh
$ ssh-keygen -t rsa -b 2048 -C "email@example.com"
$ cat ~/.ssh/id_rsa.pub
```
Paste the content of catting to gitlab: Dettings ->  SSH Keys
#### clone / download
If the system has git command, use git clone to fetch dotfiles repos.
```sh
$ git clone git@gitlab.com:valhein256/dotfiles.git
```
Or you could download the repos from gitlab.
#### Homebrew
Scripts in dotfiles.
```sh
$ cd /path/to/dotfiles
$ ./scripts/install_brew.sh
```
Or, go to [Homebrew].
After install howebrew, run the scripts: scripts/install_packages.py to install required packages.
```sh
$ cd /path/to/dotfiles
$ ./scripts/install_packages.py
```
Make sure you have installed python3 and pip3.
Todo:
Use Homebrew to install zsh and git.

##### Error case
If you encountered following problem when the script:./scripts/install_packages.py was running
```sh
Error: The following directories are not writable by your user:
/usr/local/share/zsh
/usr/local/share/zsh/site-functions

You should change the ownership of these directories to your user.
  sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions
```

#### Font and Theme
##### Font
Ref: https://github.com/Homebrew/homebrew-cask-fonts
```sh
$ brew tap homebrew/cask-fonts && brew cask install font-saucecodepro-nerd-font # Install Source Code Pro With Nerd Font.
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
# Others
### Init git submodule
```sh
$ ./scripts/git_submodule_add.sh
```
* git submodule add https://github.com/zplug/zplug zsh/zplug
* git submodule add https://github.com/tmux-plugins/tpm tmux/plugins/tpm
### Vim and Neovim setting
Todo: [Use my old vimrc for NeoVim]
Ref:
    1. https://blog.m157q.tw/posts/2018/07/23/use-my-old-vimrc-for-neovim/

### Other Documents
[What is the difference between venv, pyvenv, pyenv, virtualenv, virtualenvwrapper, pipenv, etc?]

   [Chrome]: <https://www.google.com/chrome/?brand=CHBD&gclid=CjwKCAjw34n5BRA9EiwA2u9k30fBEMblRcv82Os1vwt6z4tOarneYbf-eOGCF4Uy7kVNs4MxcmpE6xoC4lUQAvD_BwE&gclsrc=aw.ds>
   [Firfox]: <https://www.mozilla.org/en-US/>
   [Docker]: <https://www.docker.com/>
   [virtualbox]: <https://www.virtualbox.org/>
   [vagrant]: <https://www.vagrantup.com/>
   [iTerm2]: <https://www.iterm2.com/>
   [Homebrew]: <https://brew.sh/>
   [iterm2-color-schemes]: <https://iterm2colorschemes.com/>
   [Use my old vimrc for NeoVim]: <https://blog.m157q.tw/posts/2018/07/23/use-my-old-vimrc-for-neovim/>
   [What is the difference between venv, pyvenv, pyenv, virtualenv, virtualenvwrapper, pipenv, etc?]: <https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe/41573588#41573588>
