#!/bin/bash

cat > ~/.tmux.conf << 'EOF'
# Custom tmux Configuration
# Configured for enhanced terminal multiplexer usage

# Change prefix key from C-b to C-a
unbind C-b
set-option -g prefix C-a
bind-key C-a send-prefix

# Split panes with | and -
bind-key | split-window -h
bind-key - split-window -v

# Reload configuration with r
bind-key r source-file ~/.tmux.conf

# Alt+Arrow pane navigation (root table, no prefix needed)
bind-key -n M-Left select-pane -L
bind-key -n M-Right select-pane -R

# Enable mouse support
set -g mouse on

# Vi-style copy mode keys
set-window-option -g mode-keys vi

# Window base index starts at 1
set-option -g base-index 1
EOF

echo "tmux configuration created at ~/.tmux.conf"
