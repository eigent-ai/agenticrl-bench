#!/bin/bash

# Step 1: Source nvm in the current shell session
export HOME=/root
export NVM_DIR="$HOME/.nvm"
source "$NVM_DIR/nvm.sh"

# Step 2: Install Node.js v20 (LTS)
echo "Installing Node.js v20..."
nvm install 20

# Step 3: Install Node.js v18
echo "Installing Node.js v18..."
nvm install 18

# Step 4: Set Node.js v20 as the default version
echo "Setting default to v20..."
nvm alias default 20
nvm use default

# Step 5: Install build-essential and python3 for native module compilation
echo "Installing build dependencies..."
apt-get update
apt-get install -y build-essential python3

# Verify
echo "nvm version: $(nvm --version)"
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"
nvm list

echo "Setup complete!"
