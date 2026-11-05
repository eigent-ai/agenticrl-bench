#!/bin/bash
set -e
echo "Updating package lists..."
apt-get update -qq
echo "Installing project dependencies..."
apt-get install -y --no-install-recommends git curl
echo "Verifying tools..."
git --version
curl --version
echo "Project setup complete!"
