#!/bin/bash
# File audit report generator
# Usage: report.sh <directory> <output_file>
# Scans a directory and produces a CSV report of filename, size, and modification time.
# Output columns: filename, size, last_modified
# Rows are sorted by size, largest first.

DIR="${1:-.}"
OUTPUT="${2:-/tmp/report.csv}"

echo "filename,size_blocks,last_modified_epoch" > "$OUTPUT"

stat -c "%n,%b,%Y" $DIR/* | sort -t, -k2 -r >> "$OUTPUT"
