### Update

Update plugins (super simple)

```
nvim
:PlugUpdate
```

(Optional) Clean plugins - Deletes unused plugins

```
nvim
:PlugClean
```

(Optional) Check, download and install the latest vim-plug

```
nvim
:PlugUpgrade
```

(Optional) Pull my updates if you want my new modifications

```sh
git pull
cp init.vim ~/.config/nvim/
```

## Note

### For Non-GUI Users

* Colorschemes may not be rendered
* Changing fonts may be harder (https://unix.stackexchange.com/a/49823), if you do not intend to do customize your font, you should uncomment the devicons plugin within "init.vim" (`" Plug 'ryanoasis/vim-devicons'`)

### Mapped Commands in Normal Mode

Most custom commands expand off my map leader, keeping nvim as vanilla as possible.

* `,` - Map leader, nearly all my custom mappings starts with pressing the comma key
* `,q` - Sidebar filetree viewer (NERDTree)
* `,w` - Sidebar classes, functions, variables list (TagBar)
* `\`  - Toggle both NERDTree and TagBar
* `,ee` - Change colorscheme (with fzf fuzzy finder)
* `,ea` - Change Airline theme
* `,e1` - Color mode: Dracula (Dark)
* `,e2` - Color mode: Seoul256 (Between Dark & Light)
* `,e3` - Color mode: Forgotten (Light)
* `,e4` - Color mode: Zazen (Black & White)
* `,r` - Refresh/source ~/.config/nvim/init.vim
* `,t` - Trim all trailing whitespaces
* `,a` - Auto align variables (vim-easy-align), eg. do `,a=` while your cursor is on a bunch of variables to align their equal signs
* `,s` - New terminal in horizontal split
* `,vs` - New terminal in vertical split
* `,d` - Automatically generate Python docstrings while cursor is hovering above a function or class
* `,f` - Fuzzy find a file (fzf)
* `,g` - Toggle Goyo mode (Goyo), super clean and minimalistic viewing mode
* `,h` - Toggle rainbow parentheses highlighting
* `,j` - Set filetype to "journal" which makes the syntax highlighting beautiful when working on regular text files and markdown
* `,k` - Toggle coloring of hex colors
* `,l` - Toggle Limelight mode (Limelight), highlight the lines near cursor only
* `,c<Space>` - Toggle comment for current line (Nerd Commenter)
* `<Alt-r>` - Toggle RGB color picker
* `<Tab>` - Next buffer
* `<Shift-Tab>` - Previous buffer

More commmands at https://github.com/Optixal/.vim/blob/master/reference/commands_vim.txt

