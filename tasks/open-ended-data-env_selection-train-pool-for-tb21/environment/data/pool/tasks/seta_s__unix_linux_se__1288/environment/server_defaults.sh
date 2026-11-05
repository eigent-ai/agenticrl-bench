# Server-wide shell defaults
# Deployed by configuration management - do not edit on individual hosts

HISTFILE=/dev/null
HISTCONTROL=ignoreboth
export HISTFILE HISTCONTROL

# Standard umask for shared development servers
umask 022
