#!/bin/bash
echo 'set -g default-terminal "screen-256color"' >> ~/.tmux.conf
sed -i 's/^export TERM=xterm$/export TERM=xterm-256color/' ~/.bashrc
