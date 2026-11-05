#!/bin/bash

# Update package lists
apt-get update

# Install CMake from the default Ubuntu 24.04 repositories (provides 3.28+)
apt-get install -y cmake

# Verify installation
cmake --version

# Generate build files for the test project
mkdir -p /app/test_project/build
cd /app/test_project/build
cmake ..
