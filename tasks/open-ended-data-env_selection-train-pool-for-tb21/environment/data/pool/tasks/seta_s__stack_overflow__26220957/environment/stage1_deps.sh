#!/bin/bash
set -e

STAGE_DIR="$1"

echo "Checking required tools..."

for tool in gcc make python3; do
    if ! command -v "$tool" &> /dev/null; then
        echo "ERROR: Required tool '$tool' not found"
        exit 1
    fi
    echo "  Found: $tool ($(which $tool))"
done

echo "All required tools found."
echo "deps check passed" > "$STAGE_DIR/deps.log"
