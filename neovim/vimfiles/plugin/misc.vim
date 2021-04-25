" Airline: {{{
let g:airline_powerline_fonts = 0
let g:airline_detect_modified = 1
let g:airline_detect_paste = 1
let g:airline_detect_iminsert = 0
let g:airline#extensions#whitespace#enabled = 0

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

" VimFiler: {{{
let g:vimfiler_as_default_explorer = 1

if has("gui_macvim")
	" Like Textmate icons.
	let g:vimfiler_tree_leaf_icon = ' '
	let g:vimfiler_tree_opened_icon = '▾'
	let g:vimfiler_tree_closed_icon = '▸'
	let g:vimfiler_file_icon = '-'
	let g:vimfiler_marked_file_icon = '*'
endif

nnoremap <leader>f :VimFiler<CR>
nnoremap <leader>ff :VimFilerExplorer<CR>

" }}}
" Markdown: {{{
let g:vim_markdown_folding_disabled=1
" }}}
" Doxygentoolkit: {{{

nnoremap <leader>d :Dox<CR>

" }}}
" ClangFormant: {{{
let g:clang_format#style_options = {
            \ "BasedOnStyle": "LLVM",
            \ "PointerAlignment": "Left",
            \ "UseTab": "Never",
            \ "BreakBeforeBraces": "Allman",
            \ "Standard" : "C++11" }

"" map to <Leader>cf in C++ code
autocmd FileType c,cpp,objc nnoremap <buffer><Leader>cf :<C-u>ClangFormat<CR>
autocmd FileType c,cpp,objc vnoremap <buffer><Leader>cf :ClangFormat<CR>

"" if you install vim-operator-user
autocmd FileType c,cpp,objc map <buffer><Leader>x <Plug>(operator-clang-format)

" }}}
" VimShell: {{{
let g:vimshell_prompt = "$ "
let g:vimshell_user_prompt = 'getcwd()'
" }}}
" Tabline: {{{
hi TabLine      ctermfg=Black  ctermbg=Green     cterm=NONE
hi TabLineFill  ctermfg=Black  ctermbg=Green     cterm=NONE
hi TabLineSel   ctermfg=White  ctermbg=DarkBlue  cterm=NONE
" }}}
" Haskell-Vim: {{{
"let g:haskell_enable_quantification = 1
"let g:haskell_enable_arrowsyntax = 1
"let g:haskell_indent_where = 6
"let g:haskell_indent_do = 3
"let g:haskell_enable_pattern_synonyms = 1
" }}}
" LaTex-Box: {{{
let g:LatexBox_latexmk_preview_continuously = 1
autocmd Filetype tex noremap  <silent><leader>ll :silent !/Applications/Skim.app/Contents/SharedSupport/displayline
  \ <C-R>=line('.')<CR> "<C-R>=LatexBox_GetOutputFile()<CR>" "%:p" <CR>
let g:LatexBox_viewer = 'open -a /Applications/Skim.app'
let g:LatexBox_latexmk_options = "-pdflatex='xelatex -file-line-error -shell-escape -synctex=1'"
let $PATH .= ":/Library/TeX/texbin"

autocmd Filetype tex noremap <silent><F5> :Latexmk<CR>
" }}}
" Syntastic: {{{
nnoremap <leader>e :Errors<CR>
nnoremap <Leader>ee :SyntasticToggleMode<CR>

" Set python3 with YouCompleteMe
if has("mac")
let g:syntastic_cpp_compiler = 'clang++'
let g:syntastic_cpp_compiler_options = ' -std=c++11 -stdlib=libc++ -I./inc'
else
let g:syntastic_cpp_compiler = 'g++'
let g:syntastic_cpp_compiler_options = ' -Wall -Wextra'
let g:syntastic_c_compiler = 'gcc'
let g:syntastic_c_compiler_options = ' -Wall -Wextra'
endif

"set statusline+=%#warningmsg#
"set statusline+=%{SyntasticStatuslineFlag()}
"set statusline+=%*

let g:syntastic_always_populate_loc_list = 0
let g:syntastic_auto_loc_list = 0
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 0
let g:syntastic_auto_loc_list = 0

"let g:syntastic_enable_signs = 0
"let g:syntastic_enable_balloons = 0
"let g:syntastic_enable_highlighting = 0
"let g:syntastic_enable_highlighting = 0
"let g:syntastic_echo_current_error = 0
" }}}
" Tagbar:{{{
nmap <F8> :TagbarToggle<CR>
" }}}

" Ack:{{{
let g:ackprg = 'ag --nogroup --nocolor --column'
" }}}

" CtrlSF:{{{
nmap     <C-F>f <Plug>CtrlSFPrompt
vmap     <C-F>f <Plug>CtrlSFVwordPath
vmap     <C-F>F <Plug>CtrlSFVwordExec
nmap     <C-F>n <Plug>CtrlSFCwordPath
nmap     <C-F>p <Plug>CtrlSFPwordPath
nnoremap <C-F>o :CtrlSFOpen<CR>
nnoremap <C-F>t :CtrlSFToggle<CR>
inoremap <C-F>t <Esc>:CtrlSFToggle<CR>

let g:ctrlsf_auto_close = 0
let g:ctrlsf_position = 'bottom'
let g:ctrlsf_winsize = '30%'
" }}}
" vim: ft=vim foldmethod=marker foldcolumn=1
