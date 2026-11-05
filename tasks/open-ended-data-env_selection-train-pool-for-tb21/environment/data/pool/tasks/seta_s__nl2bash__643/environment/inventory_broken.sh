#!/bin/bash
# Media Storage Inventory Script
# Generates manifest of media files for storage migration

OUTPUT_DIR="/opt/migration/output"
mkdir -p "$OUTPUT_DIR"

# Generate inventory manifest
find /storage -name "*.mp4" -type f -o -name "*.flv" | sort | head -n 500 > "$OUTPUT_DIR/manifest.txt"

# Compute delta (entries not yet migrated)
comm -23 "$OUTPUT_DIR/manifest.txt" <(sort /opt/migration/already_migrated.txt) > "$OUTPUT_DIR/delta.txt"
