#!/bin/bash

INCOMING_DIR="/data/incoming"
ARCHIVE_DIR="/data/archive/reports"

echo "Starting file organization..."

for f in $(find "$INCOMING_DIR" -name "*_report_*" -type f); do
    echo "Moving: $f"
    mv "$f" "$ARCHIVE_DIR/"
done

echo "Organization complete."
