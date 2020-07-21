" Plugin: {{{
filetype plugin indent on

if &compatible
    set nocompatible               " Be iMproved
endif

" Required:
call plug#begin('~/.vim/plugged')

"" Apperence
Plug 'tomasr/molokai'
Plug 'w0ng/vim-hybrid'
Plug 'nanotech/jellybeans.vim'
Plug 'chriskempson/tomorrow-theme', {'rtp': 'vim'}
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
Plug 'mkitt/tabline.vim'
Plug 'dracula/vim', { 'as': 'dracula' }
Plug 'cocopon/iceberg.vim'

" Generic
Plug 'Shougo/vimproc.vim', {'do': 'make'}
Plug 'Shougo/vimfiler.vim'
Plug 'sheerun/vim-polyglot'

"" Edit
Plug 'scrooloose/syntastic'
Plug 'MarcWeber/vim-addon-mw-utils'
Plug 'tpope/vim-surround'
Plug 'tpope/vim-endwise'
Plug 'tpope/vim-speeddating'
Plug 'tpope/vim-sensible'
Plug 'majutsushi/tagbar'
Plug 'scrooloose/nerdcommenter'
Plug 'Raimondi/delimitMate'
Plug 'michaeljsmith/vim-indent-object'
Plug 'vim-scripts/DoxygenToolkit.vim', {'for': 'cpp'}
Plug 'ntpeters/vim-better-whitespace'
Plug 'rizzatti/dash.vim'
Plug 'plasticboy/vim-markdown', {'for': 'mkd'}
Plug 'iamcco/markdown-preview.vim',
Plug 'vim-scripts/cscope.vim'

"" Haskell
Plug 'ujihisa/neco-ghc', {'for': 'haskell'}
Plug 'ujihisa/repl.vim', {'for': 'haskell'}
Plug 'eagletmt/ghcmod-vim', {'for': 'haskell'}
Plug 'vim-scripts/haskell.vim', {'for': 'haskell'}

"" C/ Cpp
Plug 'rhysd/vim-clang-format', {'for': 'cpp'}

"" Python
Plug 'klen/python-mode', {'for': 'python'}
Plug 'hdima/python-syntax', {'for': 'python'}
Plug 'nvie/vim-flake8',  {'for': 'python'}

"" Golang
Plug 'fatih/vim-go', { 'do': ':GoUpdateBinaries' }

"" Node
Plug 'moll/vim-node', {'for': 'node'}

"" Git
Plug 'tpope/vim-fugitive'
Plug 'int3/vim-extradite'
Plug 'junegunn/gv.vim', {'on': 'GV'}

"" Trace code.
Plug 'mileszs/ack.vim'
Plug 'dyng/ctrlsf.vim'

"" Search {{{
Plug 'Shougo/unite.vim'
Plug 'Shougo/neomru.vim'
Plug 'Shougo/neoyank.vim'
Plug 'thinca/vim-unite-history'
Plug 'Shougo/unite-outline'
" }}}
"
"" Autocomplete {{{
Plug 'Valloric/YouCompleteMe', {'do': './install.py --clang-completer'}
Plug 'rdnetto/YCM-Generator'
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'
" }}}

call plug#end()

" }}}
" Autocomplete: {{{
source ~/.vim/vim/plugin/autocomplete.vim
" }}}
" Search: {{{
source ~/.vim/vim/plugin/search.vim
" }}}
" Misc: {{{
source ~/.vim/vim/plugin/misc.vim
" }}}

" vim: ft=vim foldmethod=marker foldcolumn=1
