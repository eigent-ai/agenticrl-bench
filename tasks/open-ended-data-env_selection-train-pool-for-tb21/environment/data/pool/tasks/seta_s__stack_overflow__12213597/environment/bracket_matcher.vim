" Bracket matcher plugin
" Provides a function to jump to matching brackets

if exists('g:bracket_matcher_loaded')
    finish
endif

function! BracketMatchJump()
    let l:char = getline('.')[col('.') - 1]
    if l:char == '(' || l:char == ')'
        call searchpair('(', '', ')', 'W')
    elseif l:char == '[' || l:char == ']'
        call searchpair('\[', '', '\]', 'W')
    elseif l:char == '{' || l:char == '}'
        call searchpair('{', '', '}', 'W')
    endif
endfunction

nnoremap <silent> <Leader>b :call BracketMatchJump()<CR>

let g:bracket_matcher_loaded = 1
