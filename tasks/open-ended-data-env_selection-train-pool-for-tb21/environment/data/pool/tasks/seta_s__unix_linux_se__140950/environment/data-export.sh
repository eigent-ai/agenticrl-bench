#!/bin/bash
# Data export job
OUTPUT_DIR="/var/spool/jobs/output"
mkdir -p "$OUTPUT_DIR"
echo "Starting data export at $(date)" > "$OUTPUT_DIR/data-export.log"
for i in $(seq 1 10); do
    echo "Processing batch $i of 10..." >> "$OUTPUT_DIR/data-export.log"
    sleep 1
done
echo "Data export complete at $(date)" >> "$OUTPUT_DIR/data-export.log"
