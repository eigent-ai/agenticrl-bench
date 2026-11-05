#!/bin/bash
# Fix APT repository architecture configuration for three specific files

# 1. Fix deadsnakes.list - add arch=amd64 inside existing brackets
sed -i 's/\[trusted=yes\]/[arch=amd64 trusted=yes]/' /etc/apt/sources.list.d/deadsnakes.list

# 2. Fix nodesource.list - add arch=amd64 inside existing brackets
sed -i 's/\[signed-by/[arch=amd64 signed-by/' /etc/apt/sources.list.d/nodesource.list

# 3. Fix google-chrome.sources - add Architectures field after Types line
sed -i '/^Types:/a Architectures: amd64' /etc/apt/sources.list.d/google-chrome.sources

# Verify
apt-get update
