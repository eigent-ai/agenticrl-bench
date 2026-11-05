#!/bin/bash
BACKUP_DIR="/opt/backups"
REPORT="${BACKUP_DIR}/logs/quarterly_$(date +%Y_Q$(( ($(date +%-m) - 1) / 3 + 1 ))).report"
echo "Quarterly Report - Generated $(date)" > "$REPORT"
echo "=================================" >> "$REPORT"
echo "Total backups this quarter: $(ls ${BACKUP_DIR}/logs/full_backup_*.marker 2>/dev/null | wc -l)" >> "$REPORT"
echo "Report generation complete." >> "$REPORT"
