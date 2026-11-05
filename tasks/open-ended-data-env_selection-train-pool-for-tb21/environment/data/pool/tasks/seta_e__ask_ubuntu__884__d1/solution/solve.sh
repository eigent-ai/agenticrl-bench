#!/bin/bash

# Step 1: Download Docker's GPG key and dearmor it
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod 644 /etc/apt/keyrings/docker.gpg

# Step 2: Fix NodeSource repository to use signed-by instead of trusted=yes
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list

# Step 3: Verify apt-get update works without GPG errors
apt-get update
