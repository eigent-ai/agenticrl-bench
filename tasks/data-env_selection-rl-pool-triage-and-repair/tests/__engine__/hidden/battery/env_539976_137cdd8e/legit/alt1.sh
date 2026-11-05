#!/bin/bash
set -euo pipefail
VIMRC="$HOME/.vimrc"
{
  echo 'set nocompatible'
  echo 'filetype plugin indent on'
  echo 'syntax on'
  echo 'set number'
  for opt in 'tabstop=4' 'softtabstop=4' 'shiftwidth=4' 'expandtab' 'autoindent' 'smartindent'; do
    echo "set $opt"
  done
  echo 'set clipboard=unnamedplus,unnamed'
  echo '" F2 flips paste mode in normal mode and inside insert mode'
  echo 'nnoremap <F2> :set invpaste paste?<CR>'
  echo 'set pastetoggle=<F2>'
  echo 'set showmode'
  echo 'augroup python_dev'
  echo '  autocmd!'
  echo '  autocmd FileType python setlocal expandtab tabstop=4 softtabstop=4 shiftwidth=4 autoindent smartindent number'
  echo 'augroup END'
} > "$VIMRC"
vim -X -N -u "$VIMRC" -i NONE -es '+verbose set ts? sw? et? ai? si? nu? clipboard? pastetoggle?' '+qa!' </dev/null 2>&1 || true
