#!/bin/bash
# Storage Audit Report Generator v2.1
# Generates disk usage report for image files

CONF_FILE="/etc/storage-audit/audit.conf"
SCAN_DIR=$(grep "^scan_directories" "$CONF_FILE" | cut -d= -f2)
OUTPUT=$(grep "^output_file" "$CONF_FILE" | cut -d= -f2)

# Find all jpg files and get their sizes
RESULTS=""
for f in $(find $SCAN_DIR -name '*.jpg' -exec du -s {} \;); do
    RESULTS="$RESULTS\n$f"
done

# Write report
echo -e "$RESULTS" > "$OUTPUT"

echo "Report generated at $OUTPUT"
