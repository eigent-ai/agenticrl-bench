#!/bin/bash
cat > ~/.vimrc <<'V'
syntax on
filetype plugin indent on
set number
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent
set pastetoggle=<F2>
V
