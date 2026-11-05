#!/bin/bash
#
# Concatenation processor - copies source file content to named output
#

SOURCE="$1"
OUTPUT_NAME="$2"
OUTPUT_DIR="/opt/filewatch/out"

if [ -z "$SOURCE" ] || [ -z "$OUTPUT_NAME" ]; then
    echo "Usage: concat.sh <source_file> <output_name>" >&2
    exit 1
fi

if [ ! -f "$SOURCE" ]; then
    echo "Source file not found: $SOURCE" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
cp "$SOURCE" "$OUTPUT_DIR/$OUTPUT_NAME"
exit $?
