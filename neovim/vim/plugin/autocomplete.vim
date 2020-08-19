" Autocomplete: {{{
    " UltiSnips: {{{
    " Trigger configuration. Do not use <tab> if you use https://github.com/Valloric/YouCompleteMe.
    let g:UltiSnipsExpandTrigger="<c-l>"
    let g:UltiSnipsJumpForwardTrigger="<c-j>"
    let g:UltiSnipsJumpBackwardTrigger="<c-z>"

    let g:ycm_key_list_select_completion=[]
    let g:ycm_key_list_previous_completion=[]

    " If you want :UltiSnipsEdit to split your window.
    let g:UltiSnipsEditSplit="vertical"
    " }}}
    " YouCompleteMe: {{{
    let g:ycm_global_ycm_extra_conf = "~/.vim/.ycm_extra_conf.py"
    let g:ycm_autoclose_preview_window_after_insertion = 1
    let g:ycm_confirm_extra_conf = 0

    let g:ycm_enable_diagnostic_highlighting = 0
    let g:ycm_show_diagnostics_ui = 0
    let g:ycm_enable_diagnostic_signs = 0

    " mapping
    nnoremap <leader>gs :YcmDiags<cr>
    nnoremap <leader>gd :YcmCompleter GoToDeclaration<cr>
    nnoremap <leader>gf :YcmCompleter GoToDefinition<cr>
    nnoremap <leader>gg :YcmCompleter GoToDefinitionElseDeclaration<cr>
    " }}}

" }}}

" vim: ft=vim foldmethod=marker foldcolumn=1
