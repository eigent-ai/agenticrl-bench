#!/bin/bash
# Select printable report files from the archive directory
# Reports are identified by their .rpt extension

ARCHIVE_DIR="$1"
OUTPUT_FILE="$2"

if [ -z "$ARCHIVE_DIR" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <archive_dir> <output_file>"
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "Error: Directory not found: $ARCHIVE_DIR"
    exit 1
fi

# Find all report files by extension
find "$ARCHIVE_DIR" -name "*.rpt" -type f > "$OUTPUT_FILE"

FOUND=$(wc -l < "$OUTPUT_FILE")
echo "Found $FOUND report files"
exit 0
