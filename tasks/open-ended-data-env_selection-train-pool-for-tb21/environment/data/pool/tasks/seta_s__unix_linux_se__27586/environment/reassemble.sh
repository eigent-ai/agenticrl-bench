#!/bin/bash
# Reassembles log chunks into a single file.
# Usage: reassemble.sh <chunk_dir> <output_file>

CHUNK_DIR="$1"
OUTPUT="$2"

if [ -z "$CHUNK_DIR" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <chunk_dir> <output_file>" >&2
    exit 1
fi

mkdir -p "$(dirname "$OUTPUT")"
cat "${CHUNK_DIR}/part_*" > "$OUTPUT"
echo "Reassembled to: $OUTPUT ($(stat -c '%s' "$OUTPUT") bytes)"
