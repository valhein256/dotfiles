" zM: fold all
" zR: unfold all

" Esc Keymapping: {{{
inoremap jk <esc>
" "}}}
" General: {{{
"" auto reload vimrc when editing it
autocmd! bufwritepost .vimrc source ~/.vimrc

syntax enable
set t_Co=256            " 256 color mode
"set background=dark
"color Tomorrow-Night-Bright
"color airline 
colorscheme dracula

set ttyfast
set number

set autoread            " auto reload file when the file content is changed

set ruler               " show the cursor position all the time
set autoread            " auto read when file is changed from outside

filetype on             " Enable filetype detection
filetype plugin on      " Enable filetype-specific plugins
filetype indent on      " Enable filetype-specific indenting

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

" "}}}
" Set_encoding: {{{
set encoding=utf-8
set fileencoding=utf-8
set termencoding=utf-8
set ambiwidth=double
" "}}}
" Disable_sound_on_errors: {{{
set noerrorbells
set novisualbell
set tm=500
" "}}}
" Search: {{{
set showcmd
set incsearch
set showmatch
set ignorecase
set smartcase

set hls

nnoremap <ESC>u :nohl<CR>
" "}}}
" Folding: {{{
set foldnestmax=5
set foldcolumn=2
set foldmethod=syntax
set foldlevel=99
" "}}}
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
" "}}}
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

" "}}}
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

" "}}}
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
endif
" "}}}
" Programming: {{{
"" Restore cursor to file position in previous editing session
set viminfo='10,\"100,:20,%,n~/.viminfo
au BufReadPost * if line("'\"") > 0|if line("'\"") <= line("$")|exe("norm'\"")|else|exe "norm $"|endif|endif

"" Auto remove each line-end space
augroup kill_trailing_whitespace
  au!
  autocmd FileType c,java,php,cabal,cpp,haskell,javascript,php,python,readme,text
    \ autocmd BufWritePre <buffer>
    \ :call setline(1,map(getline(1,"$"),'substitute(v:val,"\\s\\+$","","")'))
augroup END

set completeopt-=preview

" "}}}
" Auto Swith-Paste: {{{
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

" vim: ft=vim foldmethod=marker foldcolumn=1
