#!/bin/bash
set -euo pipefail

REPORT_DIR="/var/reports"
REPORT_FILE="$REPORT_DIR/system_stats.txt"

mkdir -p "$REPORT_DIR"

echo "=== System Statistics Report ===" > "$REPORT_FILE"
echo "Generated: $(date -Iseconds)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "--- Shadow Entries ---" >> "$REPORT_FILE"
sudo wc -l /etc/shadow >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "--- Disk Usage ---" >> "$REPORT_FILE"
sudo df -h / >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "--- Listening Ports ---" >> "$REPORT_FILE"
sudo ss -tlnp >> "$REPORT_FILE"

echo "" >> "$REPORT_FILE"
echo "=== Report Complete ===" >> "$REPORT_FILE"
