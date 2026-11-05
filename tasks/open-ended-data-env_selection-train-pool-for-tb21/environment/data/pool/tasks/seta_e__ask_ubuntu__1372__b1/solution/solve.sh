#!/bin/bash

# Create or update the system-wide zsh environment file
# /etc/zsh/zshenv is sourced BEFORE the user's ~/.zshenv, which means
# it runs before user2's "unsetopt GLOBAL_RCS" takes effect.
# This makes it the only system-wide zsh config that works for ALL users.

mkdir -p /etc/zsh

cat >> /etc/zsh/zshenv << 'EOF'
# Add devtools to PATH for all users
export PATH="/opt/devtools/bin:$PATH"
EOF

chmod 644 /etc/zsh/zshenv

echo "Done!"
