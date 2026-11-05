#!/bin/bash
# Project integrity verification tool
# Computes MD5 fingerprint for a project directory

if [ $# -ne 1 ]; then
    echo "Usage: $0 <project_directory>"
    exit 1
fi

DIR="$1"
if [ ! -d "$DIR" ]; then
    echo "Error: '$DIR' is not a directory"
    exit 1
fi

# Find all files, sort for deterministic order, compute fingerprint
FINGERPRINT=$(find "$DIR" -type f | sort -u | md5sum | awk '{print $1}')
echo "$FINGERPRINT"
