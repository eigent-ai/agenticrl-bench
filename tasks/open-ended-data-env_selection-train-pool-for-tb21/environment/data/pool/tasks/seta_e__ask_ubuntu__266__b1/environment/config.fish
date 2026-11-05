# Fish Shell Configuration
# Converted from .bashrc

# Set PATH
export PATH="$HOME/.local/bin:$PATH"

# Set default editor
export EDITOR=vim

# Custom greeting
if [ "$TERM" != "dumb" ]; then
    set -g fish_greeting "Welcome to Fish shell"
fi

# Add custom bin to path
if [ -d "$HOME/bin" ]; then
    export PATH="$HOME/bin:$PATH"
fi

# Source bash aliases (leftover from migration)
if [ -f ~/.bash_aliases ]; then
    source ~/.bash_aliases
fi
