#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/output"
MANIFEST="$OUTPUT_DIR/manifest.txt"

> "$MANIFEST"

cd "$OUTPUT_DIR"

for file in $(ls -t); do
    [ "$file" = "manifest.txt" ] && continue

    size=$(stat --format='%s' $file)
    size_bits=$(expr $size \* 8)

    echo "$file $size $size_bits" >> "$MANIFEST"
done

echo "Manifest written to $MANIFEST"
exit 0
