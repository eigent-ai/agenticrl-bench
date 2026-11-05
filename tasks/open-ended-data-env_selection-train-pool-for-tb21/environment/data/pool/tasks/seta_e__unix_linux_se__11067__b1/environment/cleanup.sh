#!/bin/bash
LOG=/mnt/logvol/access.log
TMP=/mnt/logvol/access.log.tmp

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting nginx access log cleanup"
echo "  Current log size : $(du -sh "$LOG" | cut -f1)"
echo "  Partition free   : $(df -h /mnt/logvol | awk 'NR==2{print $4}')"

awk '$7 !~ /^\/internal\//' "$LOG" > "$TMP" && \
    mv "$TMP" "$LOG" && \
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done. New size: $(du -sh "$LOG" | cut -f1)" || \
    { rm -f "$TMP"; echo "[$(date '+%Y-%m-%d %H:%M:%S')] FAILED -- see above"; exit 1; }
