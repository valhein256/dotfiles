" Python autocomplete setting
let python_highlight_all = 1
syntax on

"autocmd BufRead,BufNewFile *.py map <F9> :% w !python<CR>
"autocmd BufRead,BufNewFile *.py vmap f :w !python<CR>
"autocmd FileType python set complete+=k~/.vim/syntax/python.vim isk+=.,(

autocmd FileType python setlocal foldmethod=indent
set foldlevel=99

" Set python3 with YouCompleteMe
if has("mac")
let g:ycm_python_binary_path = '/usr/local/bin/python3'
let g:syntastic_python_python_exec = '/usr/local/bin/python3'
else
let g:ycm_python_binary_path = '/usr/bin/python3'
let g:syntastic_python_python_exec = '/usr/bin/python3'
endif


" Python-mode
" Activate rope
" Keys:
" K             Show python docs
" <Ctrl-Space>  Rope autocomplete
" <Ctrl-c>g     Rope goto definition
" <Ctrl-c>d     Rope show documentation
" <Ctrl-c>f     Rope find occurrences
" <Leader>b     Set, unset breakpoint (g:pymode_breakpoint enabled)
" [[            Jump on previous class or function (normal, visual, operator modes)
" ]]            Jump on next class or function (normal, visual, operator modes)
" [M            Jump on previous class or method (normal, visual, operator modes)
" ]M            Jump on next class or method (normal, visual, operator modes)
let g:pymode_rope = 0

" Documentation
let g:pymode_doc = 0
let g:pymode_doc_key = 'K'

" Load run code plugin
let g:pymode_run = 0

" Run python code
"let g:pymode_run_key = '<leader>r'

" Disable code checking
let g:pymode_lint = 0
let g:pymode_lint_on_write = 0

" Support virtualenv
let g:pymode_virtualenv = 1

" Enable breakpoints plugin
let g:pymode_breakpoint = 1
let g:pymode_breakpoint_key = '<leader>b'

" syntax highlighting
let g:pymode_syntax = 1
let g:pymode_syntax_all = 1
let g:pymode_syntax_indent_errors = g:pymode_syntax_all
let g:pymode_syntax_space_errors = g:pymode_syntax_all

" Don't autofold code
let g:pymode_folding = 0


" set python indention
setlocal tabstop=4
setlocal softtabstop=4
setlocal shiftwidth=4
setlocal textwidth=79
setlocal expandtab
setlocal autoindent
setlocal fileformat=unix
