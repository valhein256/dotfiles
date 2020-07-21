""" neo-ghc setting
" Disable haskell-vim omnifunc
let g:haskellmode_completion_ghc = 0
autocmd FileType haskell setlocal omnifunc=necoghc#omnifunc

""" For YCM setting
let g:ycm_semantic_triggers = {'haskell' : ['.']}

""" Haskell map
autocmd FileType haskell nnoremap <silent><F5> :!hasktags -c .<CR>
autocmd FileType haskell nnoremap <buffer><F6> :HdevtoolsType<CR>
autocmd FileType haskell nnoremap <buffer><silent><F7> :HdevtoolsClear<CR>
autocmd FileType haskell nnoremap <buffer><silent><F8> :HdevtoolsInfo<CR>

