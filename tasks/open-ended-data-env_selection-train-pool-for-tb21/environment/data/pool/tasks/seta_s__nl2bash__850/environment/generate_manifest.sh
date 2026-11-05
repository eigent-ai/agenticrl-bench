#!/bin/bash
# generate_manifest.sh - Generate source distribution manifest
# Lists all distributable source files, excluding build artifacts

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Generating manifest for: $PROJECT_ROOT"

# Find all files, excluding common artifacts
find . -follow -type f \
    | grep -v "class" \
    | grep -v "png" \
    | grep -v "\.pyc$" \
    | grep -v "/\.git/" \
    > MANIFEST.txt

FILE_COUNT=$(wc -l < MANIFEST.txt)
echo "Manifest generated with $FILE_COUNT files -> MANIFEST.txt"
