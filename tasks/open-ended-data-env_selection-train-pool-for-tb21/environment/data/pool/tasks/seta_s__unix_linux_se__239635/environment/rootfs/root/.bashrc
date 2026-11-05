# ~/.bashrc: executed by bash(1) for non-login interactive shells.

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

shopt -s histappend

HISTCONTROL=ignoreboth
HISTSIZE=1000
HISTFILESIZE=2000

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Editor configuration — set preferred text editor for command-line tools
EDITOR=nano
# export VISUAL="$EDITOR"
