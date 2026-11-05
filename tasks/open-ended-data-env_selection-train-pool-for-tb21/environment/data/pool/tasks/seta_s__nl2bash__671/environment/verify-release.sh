#!/bin/bash
# Release integrity verification
# Computes content hash of a release directory
TARGET_DIR="${1:-.}"
find "$TARGET_DIR" | xargs cat 2>/dev/null | sha1sum | awk '{print $1}'
