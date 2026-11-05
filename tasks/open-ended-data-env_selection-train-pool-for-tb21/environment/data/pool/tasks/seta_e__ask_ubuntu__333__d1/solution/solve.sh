#!/bin/bash

# Backup the original sources.list
cp /etc/apt/sources.list /etc/apt/sources.list.bak

# Create new sources.list with mirror:// URLs for noble
cat > /etc/apt/sources.list << 'EOF'
deb mirror://mirrors.ubuntu.com/mirrors.txt noble main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt noble-updates main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt noble-backports main restricted universe multiverse
deb mirror://mirrors.ubuntu.com/mirrors.txt noble-security main restricted universe multiverse
EOF

# Verify the configuration
echo "New sources.list configuration:"
cat /etc/apt/sources.list

# Test that APT can read the new configuration
apt-get update -qq || echo "Warning: apt-get update encountered some issues"
