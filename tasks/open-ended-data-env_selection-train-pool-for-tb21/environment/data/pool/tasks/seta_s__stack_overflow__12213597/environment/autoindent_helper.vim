" Autoindent helper plugin
" Configures sensible indentation defaults

if exists('g:autoindent_helper_loaded')
    finish
endif

set autoindent
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set softtabstop=4

let g:autoindent_helper_loaded = 1
