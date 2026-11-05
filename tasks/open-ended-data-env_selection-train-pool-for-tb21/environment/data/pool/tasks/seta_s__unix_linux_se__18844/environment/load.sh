#!/bin/bash
source /opt/dataproc/config.ini
INPUT="$DATA_DIR/staging/transformed.csv"
OUTPUT="$DATA_DIR/output/report.csv"
if [ ! -f "$INPUT" ]; then
    echo "[$(date)] ERROR: Transform output not found" >> "$LOG_DIR/pipeline.log"
    exit 1
fi
cp "$INPUT" "$OUTPUT"
echo "[$(date)] Report written to $OUTPUT ($(wc -l < "$OUTPUT") lines)" >> "$LOG_DIR/pipeline.log"
