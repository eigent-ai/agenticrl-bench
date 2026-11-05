#!/bin/bash
# Report generation job
OUTPUT_DIR="/var/spool/jobs/output"
mkdir -p "$OUTPUT_DIR"
echo "Report Generation Started: $(date)" > "$OUTPUT_DIR/report-gen.log"
echo "Collecting metrics..." >> "$OUTPUT_DIR/report-gen.log"
sleep 2
echo "Generating summary..." >> "$OUTPUT_DIR/report-gen.log"
sleep 1
echo "Report complete: $(date)" >> "$OUTPUT_DIR/report-gen.log"
