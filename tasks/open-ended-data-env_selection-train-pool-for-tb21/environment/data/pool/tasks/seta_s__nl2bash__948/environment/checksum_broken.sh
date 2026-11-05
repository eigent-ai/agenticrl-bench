#!/bin/bash
# Generate SHA-256 checksums for all files in manifest
OUTPUT_DIR="/opt/pipeline/output"
DATA_DIR="/opt/pipeline/data"
rm -f "$OUTPUT_DIR/checksums.txt"
while read line; do
    checksum=$(sha256sum $DATA_DIR/$line | awk '{print $1}')
    echo "$checksum  $line" >> "$OUTPUT_DIR/checksums.txt"
done < "$OUTPUT_DIR/manifest.txt"
echo "Checksums generated for $(wc -l < "$OUTPUT_DIR/checksums.txt") files"
