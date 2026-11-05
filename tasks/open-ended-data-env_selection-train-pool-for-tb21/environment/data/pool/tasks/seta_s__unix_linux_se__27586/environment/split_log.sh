#!/bin/bash
# Splits a log file into fixed-size chunks and records a manifest.
# Usage: split_log.sh <input_file> <output_dir>

INPUT="$1"
OUTPUT_DIR="$2"

if [ -z "$INPUT" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <input_file> <output_dir>" >&2
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

split -b 50 "$INPUT" "$OUTPUT_DIR/part_"

echo "# Log chunk manifest" > "$OUTPUT_DIR/manifest.txt"
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$OUTPUT_DIR/manifest.txt"
stat -c "%n %s" -- "$OUTPUT_DIR"/part_* >> "$OUTPUT_DIR/manifest.txt"
