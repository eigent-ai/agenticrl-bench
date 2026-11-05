#!/bin/bash
# Configure useful aliases and functions
alias ll="ls -la"
alias dev="cd $DEV_HOME"
alias proj="cd $PROJECT_ROOT"

# Define a useful function
reload_env() {
    echo "Reloading environment..."
    . /app/setup_env.sh
    echo "Environment reloaded!"
}

export -f reload_env 2>/dev/null || true

echo "Aliases and functions configured"
