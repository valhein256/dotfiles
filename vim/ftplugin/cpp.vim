" automatically open and close the popup menu / preview window
au CursorMovedI,InsertLeave * if pumvisible() == 0|silent! pclose|endif
set completeopt=menuone,menu,longest,preview

" set indent - llvm style
setlocal shiftwidth=2
setlocal softtabstop=2
setlocal tabstop=2

" Disable Youcompleteme autocomplete
let g:ycm_auto_trigger = 1
let g:ycm_key_invoke_completion = '<C-l>'

"GNU Coding Standards
setlocal cindent
setlocal cinoptions=>4,n-2,{2,^-2,:2,=2,g0,h2,p5,t0,+2,(0,u0,w1,m1
setlocal expandtab
setlocal shiftwidth=2
setlocal tabstop=8
setlocal softtabstop=2
setlocal textwidth=80
setlocal fo-=ro fo+=cql

