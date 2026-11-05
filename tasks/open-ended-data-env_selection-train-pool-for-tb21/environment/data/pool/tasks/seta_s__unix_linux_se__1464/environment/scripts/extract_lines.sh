#!/bin/bash
# Usage: extract_lines.sh <source_file> <start_line> <end_line> <dest_file>

SOURCE=$1
START=$2
END=$3
DEST=$4

if [ -z "$SOURCE" ] || [ -z "$START" ] || [ -z "$END" ] || [ -z "$DEST" ]; then
    echo "Usage: $0 <source_file> <start_line> <end_line> <dest_file>" >&2
    exit 1
fi

# Extract the specified line range and append to destination
sed -n "${START},${END}" "$SOURCE" >> "$DEST"
