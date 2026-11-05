#!/bin/bash

# This script installs packages from packages.txt

zypper refresh

# Read packages from packages.txt and install them
while IFS= read -r package; do
    if [ -n "$package" ]; then
        zypper install "$package"
    fi
done < /workspace/packages.txt
