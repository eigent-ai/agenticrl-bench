#!/bin/bash
# Install nvm v0.40.1 manually
export HOME=/root
export NVM_DIR="$HOME/.nvm"
mkdir -p "$NVM_DIR"
git clone https://github.com/nvm-sh/nvm.git "$NVM_DIR"
cd "$NVM_DIR"
git checkout v0.40.1
cd /

# Add nvm initialization to bashrc
cat >> /root/.bashrc << 'BASHRC'
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
BASHRC
