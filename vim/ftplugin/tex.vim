" LaTex File Spell Check
augroup filetype
    au! BufRead,BufNewFile *.tex     set spell 
augroup END

map <silent> <Leader>ss :silent !/Applications/Skim.app/Contents/SharedSupport/displayline
        \ <C-R>=line('.')<CR> "<C-R>=LatexBox_GetOutputFile()<CR>" "%:p" <CR>
"let g:LatexBox_viewer = 'open -a /Applications/Skim.app'

set cole=0
