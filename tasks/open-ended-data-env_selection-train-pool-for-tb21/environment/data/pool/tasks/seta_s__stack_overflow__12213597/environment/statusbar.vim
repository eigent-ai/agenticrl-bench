" Statusbar plugin
" Custom status line formatting

if exists('g:statusbar_loaded')
    finish
endif

set statusline=%f\ %h%m%r%=%-14.(%l,%c%V%)\ %P
set laststatus=2

let g:statusbar_loaded = 1
