" Line numbers plugin
" Enables line number display

if exists('g:line_numbers_loaded')
    finish
endif

set number
set relativenumber

let g:line_numbers_loaded = 1
