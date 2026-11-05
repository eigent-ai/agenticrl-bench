#!/bin/bash

# Read existing bashrc and append the custom prompt configuration
cat >> /root/.bashrc << 'BASHRC_END'

# Git branch detection function
__git_prompt() {
    local branch
    branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
    if [ -n "$branch" ]; then
        if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
            # Clean working tree - bold yellow
            echo " \[\033[01;33m\]($branch)\[\033[00m\]"
        else
            # Dirty working tree - bold red
            echo " \[\033[01;31m\]($branch)\[\033[00m\]"
        fi
    fi
}

# Capture exit status before it gets overwritten
PROMPT_COMMAND='__LAST_EXIT=$?'

# Exit code indicator function
__exit_status() {
    if [ "${__LAST_EXIT:-0}" -eq 0 ]; then
        echo "\[\033[01;32m\][OK]\[\033[00m\]"
    else
        echo "\[\033[01;31m\][FAIL]\[\033[00m\]"
    fi
}

# Custom PS1 with timestamp, user, host, directory, git branch, and exit code
PS1='\[\033[0;37m\][\t]\[\033[00m\] \[\033[01;36m\]\u\[\033[00m\]@\[\033[01;32m\]\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]$(__git_prompt) $(__exit_status) \$ '
BASHRC_END

echo "Custom PS1 prompt configured successfully."
