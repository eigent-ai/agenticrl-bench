#!/bin/bash
# Generate the final sorted manifest with relative paths from archive root

RAW_FILE="$1"
ARCHIVE_DIR="$2"
OUTPUT_FILE="$3"

if [ -z "$RAW_FILE" ] || [ -z "$ARCHIVE_DIR" ] || [ -z "$OUTPUT_FILE" ]; then
    echo "Usage: $0 <raw_file> <archive_dir> <output_file>"
    exit 1
fi

if [ ! -f "$RAW_FILE" ]; then
    echo "Error: Raw file list not found: $RAW_FILE"
    exit 1
fi

# Process each file path - strip archive prefix and format
> "$OUTPUT_FILE"
for f in $(cat "$RAW_FILE"); do
    rel_path=${f#$ARCHIVE_DIR/}
    echo $rel_path >> "$OUTPUT_FILE"
done

sort -o "$OUTPUT_FILE" "$OUTPUT_FILE"

COUNT=$(wc -l < "$OUTPUT_FILE")
echo "Manifest generated with $COUNT entries"
exit 0
