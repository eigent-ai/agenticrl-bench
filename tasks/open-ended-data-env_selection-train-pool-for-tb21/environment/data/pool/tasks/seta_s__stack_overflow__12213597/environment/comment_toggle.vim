" Comment toggle plugin
" Toggles line comments for common filetypes

if exists('g:comment_toggle_loaded')
    finish
endif

function! ToggleComment()
    let l:ft = &filetype
    let l:prefix = '#'
    if l:ft == 'vim'
        let l:prefix = '"'
    elseif l:ft == 'c' || l:ft == 'cpp' || l:ft == 'java' || l:ft == 'javascript'
        let l:prefix = '//'
    endif
    let l:line = getline('.')
    if l:line =~# '^\s*' . escape(l:prefix, '/"')
        call setline('.', substitute(l:line, '^\(\s*\)' . escape(l:prefix, '/"') . '\s\?', '\1', ''))
    else
        call setline('.', substitute(l:line, '^\(\s*\)', '\1' . l:prefix . ' ', ''))
    endif
endfunction

nnoremap <silent> <Leader>c :call ToggleComment()<CR>
vnoremap <silent> <Leader>c :call ToggleComment()<CR>

let g:comment_toggle_loaded = 1
