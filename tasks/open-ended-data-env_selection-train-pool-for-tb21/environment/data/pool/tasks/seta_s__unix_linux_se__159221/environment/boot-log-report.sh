#!/bin/bash
set -euo pipefail
REPORT_DIR="/var/log/boot-reports"
mkdir -p "$REPORT_DIR"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
REPORT_FILE="${REPORT_DIR}/boot-report-${TIMESTAMP}.txt"
echo "=== Boot Log Audit Report ===" > "$REPORT_FILE"
echo "Generated: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "--- Current Boot Summary ---" >> "$REPORT_FILE"
journalctl -b 0 --no-pager -p err..emerg --output=short 2>/dev/null >> "$REPORT_FILE" || echo "No error-level messages in current boot" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "--- Previous Boot Summary ---" >> "$REPORT_FILE"
journalctl -b -1 --no-pager -p err..emerg --output=short 2>/dev/null >> "$REPORT_FILE" || echo "Previous boot logs unavailable" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "--- Journal Disk Usage ---" >> "$REPORT_FILE"
journalctl --disk-usage >> "$REPORT_FILE"
echo "Report written to ${REPORT_FILE}"
