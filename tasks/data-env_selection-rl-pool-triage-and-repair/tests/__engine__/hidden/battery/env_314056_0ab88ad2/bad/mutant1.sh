#!/bin/bash
cat > ~/.zshrc <<'Z'
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'
setopt completeinword
HISTFILE=~/.zhistory
HISTSIZE=10000
SAVEHIST=10000
setopt extendedhistory sharehistory
setopt extendedglob
setopt auto_cd
setopt interactivecomments
alias ll='ls -l'
alias la='ls -a'
alias ..='cd ..'
PS1='%n@%m %~ %# '
REPORTTIME=10
mkcd() { mkdir -p "$1" && cd "$1"; }
Z
