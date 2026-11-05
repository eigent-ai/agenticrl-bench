" SearchW: search for the word under cursor in all open buffers
" Mirrors the * key but populates the quickfix list across all buffers
function! SearchWord()
    let l:word = expand('<cWORD>')
    call setqflist([])
    silent! execute 'bufdo grepadd! ' . l:word . ' %'
    if !empty(getqflist())
        copen
    endif
endfunction

command! SearchW call SearchWord()
