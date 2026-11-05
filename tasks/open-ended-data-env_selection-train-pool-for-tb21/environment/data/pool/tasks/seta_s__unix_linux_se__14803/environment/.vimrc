" Vim configuration for development
set nocompatible
filetype plugin indent on

" Allow background buffers without saving (disabled for safety)
" set hidden

syntax enable
set laststatus=2
set ruler
set number
set showcmd

" Enhanced command-line completion
set wildmenu
set wildmode=list:longest

" Buffer navigation keybindings
nmap <F3> :bprevious<CR>
nmap <F4> :bnext<CR>
nmap <F5> :bd<CR>

" Indentation
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent

" Search
set incsearch
set hlsearch
