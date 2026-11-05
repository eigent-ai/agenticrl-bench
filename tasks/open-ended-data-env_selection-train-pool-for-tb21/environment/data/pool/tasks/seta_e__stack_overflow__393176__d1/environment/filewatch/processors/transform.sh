#!/bin/bash
#
# Transform processor - lowercases all content in a CSV file
#

SOURCE="$1"
PREFIX="$2"
OUTPUT_DIR="/opt/filewatch/output"

if [ -z "$SOURCE" ] || [ -z "$PREFIX" ]; then
    echo "Usage: transform.sh <source_file> <output_prefix>" >&2
    exit 1
fi

if [ ! -f "$SOURCE" ]; then
    echo "Source file not found: $SOURCE" >&2
    exit 1
fi

BASENAME=$(basename "$SOURCE")
OUTPUT_FILE="$OUTPUT_DIR/${PREFIX}_${BASENAME}"

mkdir -p "$OUTPUT_DIR"
tr '[:upper:]' '[:lower:]' < "$SOURCE" > "$OUTPUT_FILE"
exit $?
