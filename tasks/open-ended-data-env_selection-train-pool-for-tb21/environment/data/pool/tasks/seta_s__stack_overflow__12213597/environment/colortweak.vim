" Color tweak plugin
" Applies subtle highlight overrides for better readability

if exists('g:colortweak_loaded')
    finish
endif

highlight LineNr ctermfg=DarkGrey
highlight CursorLineNr ctermfg=Yellow cterm=bold
highlight Comment ctermfg=DarkCyan
highlight String ctermfg=Green
highlight Keyword ctermfg=Blue cterm=bold

let g:colortweak_loaded = 1
