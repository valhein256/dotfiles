" zM: fold all
" zR: unfold all

""" Python3 VirtualEnv
let g:python3_host_prog = expand('~/.config/nvim/env/bin/python')

" vim-pydocstring
let g:pydocstring_doq_path = '~/.config/nvim/env/bin/doq'

" General: {{{
"" auto reload vimrc when editing it
set ttyfast
set number

set autoread            " auto reload file when the file content is changed

set ruler               " show the cursor position all the time
set autoread            " auto read when file is changed from outside

filetype on             " Enable filetype detection
filetype plugin on      " Enable filetype-specific plugins
filetype indent on      " Enable filetype-specific indenting

"" split and vsplit
set splitbelow
set splitright

"" status line
set laststatus=2

set title
set showmode            " Show current input mode in status line
set cursorline          " Show Cursor Line in Underline
"set showtabline=2
set wildmenu            " Show autocomplete menus.

" Disable bleep!
set visualbell
set noerrorbells

"" set column width
set colorcolumn=79

set nobackup
set noswapfile

""" Coloring
syntax on
color dracula
highlight Pmenu guibg=white guifg=black gui=bold
highlight Comment gui=bold
highlight Normal gui=none
highlight NonText guibg=none

" Opaque Background (Comment out to use terminal's profile)
set termguicolors

" Transparent Background (For i3 and compton)
highlight Normal guibg=NONE ctermbg=NONE
highlight LineNr guibg=NONE ctermbg=NONE

" Trim Whitespaces
function! TrimWhitespace()
    let l:save = winsaveview()
    %s/\\\@<!\s\+$//e
    call winrestview(l:save)
endfunction

" Dracula Mode (Dark)
function! ColorDracula()
    let g:airline_theme=''
    color dracula
    IndentLinesEnable
endfunction

" Seoul256 Mode (Dark & Light)
function! ColorSeoul256()
    let g:airline_theme='silver'
    color seoul256
    IndentLinesDisable
endfunction

"" Forgotten Mode (Light)
"function! ColorForgotten()
    "" Light airline themes: tomorrow, silver, alduin
    "" Light colors: forgotten-light, nemo-light
    "let g:airline_theme='tomorrow'
    "color forgotten-light
    "IndentLinesDisable
"endfunction
" }}}

" Set_encoding: {{{
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8
" }}}

" Disable_sound_on_errors: {{{
set noerrorbells
set novisualbell
set tm=500
" }}}

" Esc Keymapping: {{{
inoremap jk <esc>
" }}}

" Search: {{{
set showcmd
set incsearch
set showmatch
set ignorecase
set smartcase
set hlsearch

set hls

nnoremap <ESC>u :nohl<CR>
" }}}

" Folding: {{{
set foldnestmax=5
set foldcolumn=2
set foldmethod=syntax
set foldlevel=99
" }}}

" Indent: {{{
set backspace=indent,eol,start
set autoindent
set expandtab
set smarttab            " insert tabs on the start of a line according to context
set shiftwidth=4
set softtabstop=4
set tabstop=4

" indent key mapping
nnoremap <tab> v>
nnoremap <s-tab> v<
vnoremap <tab> >gv
vnoremap <s-tab> <gv
" }}}

" Function_key: {{{
nnoremap <silent><F1> :tab h<CR>
nnoremap <silent><F2> :VimFiler<CR>
nnoremap <silent><F3> :Gitv<CR>
nnoremap <silent><F4> :Extradite<CR>

autocmd FileType c,cpp nmap <silent><F5> :!ctags -R --c++-kinds=+p --fields=+iaS --extra=+q . && cscope -bR<CR>
autocmd FileType python nmap <silent><F5> :!ctags -R .<CR>
autocmd FileType haskell nmap <silent><F5> :!hasktags -c .<CR>

nnoremap <silent><F6> :CurrentLineWhitespaceOn<CR>
nnoremap <silent><F7> :StripWhitespace<CR>

" }}}

" Tab_setting: {{{

"" Tab_bar_color
nnoremap <leader>tn :tabnew<CR>
nnoremap <leader>te :tabedit<SPACE>
nnoremap <leader>tm :tabmove<SPACE>
nnoremap <leader>tc :tabclose<CR>
nnoremap <C-H> :tabprev<CR>
nnoremap <C-L> :tabnext<CR>

autocmd TabLeave * let g:LastUsedTabPage = tabpagenr()
function! SwitchLastUsedTab()
    if exists("g:LastUsedTabPage")
        execute "tabnext " g:LastUsedTabPage
    endif
endfunction

nnoremap tt :call SwitchLastUsedTab()<CR>

" }}}

" Filetype: {{{
if v:version >= 704
    "" C/ CPP with doxygen
    au BufNewFile,BufRead *.c set filetype=c.cpp.doxygen
    au BufNewFile,BufRead *.cpp set filetype=cpp.doxygen
    au BufNewFile,BufRead *.tcc set filetype=cpp.doxygen  " template C++ source
    au BufNewFile,BufRead *.inc set filetype=cpp.doxygen  " header C++ source
    au BufNewFile,BufRead *.h set filetype=cpp.doxygen

    "" Markdown
    au BufNewFile,BufRead *.md set filetype=mkd.markdown
    au BufNewFile,BufRead *.mkd set filetype=mkd.markdown
    au BufNewFile,BufRead *.markdown set filetype=mkd.markdown

    "" JavaScript
    au BufNewFile,BufRead *.js set filetype=javascript.jsx

    "" Golang
    au BufRead,BufNewFile *.go set filetype=go

    " HTML, XML, Jinja
    autocmd FileType html setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType css setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType xml setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType htmldjango setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType htmldjango inoremap {{ {{  }}<left><left><left>
    autocmd FileType htmldjango inoremap {% {%  %}<left><left><left>
    autocmd FileType htmldjango inoremap {# {#  #}<left><left><left>

    " Markdown and Journal
    autocmd FileType markdown setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType journal setlocal shiftwidth=2 tabstop=2 softtabstop=2
endif
" }}}

" Programming: {{{
"" Restore cursor to file position in previous editing session
"set viminfo='10,\"100,:20,%,n~/.viminfo
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm'\"")|else|exe "norm $"|endif|endif

"" Auto remove each line-end space
augroup kill_trailing_whitespace
  au!
  autocmd FileType c,java,php,cabal,cpp,haskell,javascript,php,python,readme,text
    \ autocmd BufWritePre <buffer>
    \ :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
augroup END

set completeopt-=preview
" }}}

" Auto Swith Paste: {{{
" ref: http://blog.longwin.com.tw/2014/12/vim-linux-mac-putty-paste-mode-change-2014/
if &term =~ "xterm.*"
    let &t_ti = &t_ti . "\e[?2004h"
    let &t_te = "\e[?2004l" . &t_te
    function XTermPasteBegin(ret)
        set pastetoggle=<Esc>[201~
        set paste
        return a:ret
    endfunction
    map <expr> <Esc>[200~ XTermPasteBegin("i")
    imap <expr> <Esc>[200~ XTermPasteBegin("")
    cmap <Esc>[200~ <nop>
    cmap <Esc>[201~ <nop>
endif
" }}}

" Show Tabs: {{{
"set list
set listchars=tab:>-
" }}}

" Airline: {{{
let g:airline_powerline_fonts = 1
let g:airline_detect_modified = 1
let g:airline_detect_paste = 1
let g:airline_detect_iminsert = 0
let g:airline_section_z = ' %{strftime("%-I:%M %p")}'
let g:airline_section_warning = ''
let g:airline#extensions#whitespace#enabled = 0
"let g:airline#extensions#tabline#enabled = 1

let g:airline_mode_map = {
  \ '__' : '-',
  \ 'n'  : 'N',
  \ 'i'  : 'I',
  \ 'R'  : 'R',
  \ 'c'  : 'C',
  \ 'v'  : 'V',
  \ 'V'  : 'V',
  \ '' : 'V',
  \ 's'  : 'S',
  \ 'S'  : 'S',
  \ '' : 'S',
  \ }
" }}}

" Tabline: {{{
hi TabLine      ctermfg=Black  ctermbg=Green     cterm=NONE
hi TabLineFill  ctermfg=Black  ctermbg=Green     cterm=NONE
hi TabLineSel   ctermfg=White  ctermbg=DarkBlue  cterm=NONE
" }}}

" Other Configurations: {{{
set list listchars=trail:»,tab:»-
set fillchars+=vert:\ 
set wrap breakindent
set encoding=utf-8

" }}}

""" Plugin Configurations

" NERDTree: {{{
let NERDTreeShowHidden=1
let g:NERDTreeDirArrowExpandable = '↠'
let g:NERDTreeDirArrowCollapsible = '↡'
" }}}

" Neovim Terminal: {{{
tmap <Esc> <C-\><C-n>
tmap <C-w> <Esc><C-w>
"tmap <C-d> <Esc>:q<CR>
autocmd BufWinEnter,WinEnter term://* startinsert
autocmd BufLeave term://* stopinsert
" }}}

" Deoplete: {{{
let g:deoplete#enable_at_startup = 1
" Disable documentation window
set completeopt-=preview
" }}}

" Supertab
let g:SuperTabDefaultCompletionType = "<C-n>"

" Ultisnips
let g:UltiSnipsExpandTrigger="<C-S>"
let g:UltiSnipsJumpForwardTrigger="<Tab>"
let g:UltiSnipsJumpBackwardTrigger="<C-x>"

" EasyAlign
xmap ga <Plug>(EasyAlign)
nmap ga <Plug>(EasyAlign)

" indentLine
let g:indentLine_char = '▏'
let g:indentLine_color_gui = '#363949'

" TagBar
let g:tagbar_width = 30
let g:tagbar_iconchars = ['↠', '↡']

" fzf-vim: {{{
let g:fzf_action = {
  \ 'ctrl-t': 'tab split',
  \ 'ctrl-s': 'split',
  \ 'ctrl-v': 'vsplit' }
let g:fzf_colors =
\ { 'fg':      ['fg', 'Normal'],
  \ 'bg':      ['bg', 'Normal'],
  \ 'hl':      ['fg', 'Comment'],
  \ 'fg+':     ['fg', 'CursorLine', 'CursorColumn', 'Normal'],
  \ 'bg+':     ['bg', 'CursorLine', 'CursorColumn'],
  \ 'hl+':     ['fg', 'Statement'],
  \ 'info':    ['fg', 'Type'],
  \ 'border':  ['fg', 'Ignore'],
  \ 'prompt':  ['fg', 'Character'],
  \ 'pointer': ['fg', 'Exception'],
  \ 'marker':  ['fg', 'Keyword'],
  \ 'spinner': ['fg', 'Label'],
  \ 'header':  ['fg', 'Comment'] }
" }}}

""" Filetype-Specific Configurations
" Filetype: {{{
if v:version >= 704
    "" C/ CPP with doxygen
    au BufNewFile,BufRead *.c set filetype=c.cpp.doxygen
    au BufNewFile,BufRead *.cpp set filetype=cpp.doxygen
    au BufNewFile,BufRead *.tcc set filetype=cpp.doxygen  " template C++ source
    au BufNewFile,BufRead *.inc set filetype=cpp.doxygen  " header C++ source
    au BufNewFile,BufRead *.h set filetype=cpp.doxygen

    "" Markdown
    au BufNewFile,BufRead *.md set filetype=mkd.markdown
    au BufNewFile,BufRead *.mkd set filetype=mkd.markdown
    au BufNewFile,BufRead *.markdown set filetype=mkd.markdown

    "" JavaScript
    au BufNewFile,BufRead *.js set filetype=javascript.jsx

    "" Golang
    au BufRead,BufNewFile *.go set filetype=go

    " HTML, XML, Jinja
    autocmd FileType html setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType css setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType xml setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType htmldjango setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType htmldjango inoremap {{ {{  }}<left><left><left>
    autocmd FileType htmldjango inoremap {% {%  %}<left><left><left>
    autocmd FileType htmldjango inoremap {# {#  #}<left><left><left>

    " Markdown and Journal
    autocmd FileType markdown setlocal shiftwidth=2 tabstop=2 softtabstop=2
    autocmd FileType journal setlocal shiftwidth=2 tabstop=2 softtabstop=2
endif
" }}}

""" Custom Mappings

let mapleader=","
nmap <leader>q :NERDTreeToggle<CR>
nmap \ <leader>q
nmap <leader>w :TagbarToggle<CR>
nmap <leader>ee :Colors<CR>
nmap <leader>ea :AirlineTheme 
nmap <leader>e1 :call ColorDracula()<CR>
nmap <leader>e2 :call ColorSeoul256()<CR>
"nmap <leader>e3 :call ColorForgotten()<CR>
nmap <leader>r :so ~/.config/nvim/init.vim<CR>
nmap <leader>t :call TrimWhitespace()<CR>
xmap <leader>a gaip*
nmap <leader>a gaip*
nmap <leader>s <C-w>s<C-w>j:terminal<CR>
nmap <leader>vs <C-w>v<C-w>l:terminal<CR>
nmap <leader>d <Plug>(pydocstring)
nmap <leader>f :Files<CR>
nmap <leader>g :Goyo<CR>
nmap <leader>h :RainbowParentheses!!<CR>
nmap <leader>j :set filetype=journal<CR>
nmap <leader>k :ColorToggle<CR>
nmap <leader>l :Limelight!!<CR>
xmap <leader>l :Limelight!!<CR>
autocmd FileType python nmap <leader>x :0,$!~/.config/nvim/env/bin/python -m yapf<CR>
"nmap <leader>n :HackerNews best<CR>J
nmap <silent> <leader><leader> :noh<CR>
nmap <Tab> :bnext<CR>
nmap <S-Tab> :bprevious<CR>

"" Auto remove each line-end space
augroup kill_trailing_whitespace
  au!
  autocmd FileType c,java,php,cabal,cpp,haskell,javascript,php,python,readme,text
    \ autocmd BufWritePre <buffer>
    \ :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
augroup END

" vim: ft=vim foldmethod=marker foldcolumn=1 foldlevelstart=0
