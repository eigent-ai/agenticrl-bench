#!/bin/bash
# check-and-process.sh - Validate and clean a text file
# Usage: ./tools/check-and-process.sh <input-file>

set -e

# Load environment
source ~/.bashrc

if [ -z "$1" ]; then
    echo "Usage: $0 <input-file>"
    exit 1
fi

INPUT="$1"

if [ ! -f "$INPUT" ]; then
    echo "Error: File '$INPUT' not found"
    exit 1
fi

echo "Checking environment..."
if ! command -v "$VISUAL" > /dev/null 2>&1; then
    echo "Error: VISUAL editor '$VISUAL' not found"
    exit 1
fi

echo "Processing $INPUT..."
TMPFILE=$(mktemp /tmp/check-process.XXXXXX)
cp "$INPUT" "$TMPFILE"

$VISUAL --clean -es '+%s/\s\+$//e' "+wq" "$TMPFILE"

echo "Processed output:"
cat "$TMPFILE"
rm -f "$TMPFILE"
echo ""
echo "Done."
