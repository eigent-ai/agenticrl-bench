#!/bin/bash
set -e

# Step 1: Create the keyrings directory
mkdir -p /etc/apt/keyrings

# Step 2: Download and dearmor the NodeSource GPG key
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

# Step 3: Create the sources list file
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Step 4: Update apt cache
apt-get update

# Step 5: Install Node.js
apt-get install -y nodejs

# Step 6: Verify installation
node --version
