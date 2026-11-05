#!/bin/bash
LOGDIR="/opt/logaudit/logs"
PATTERNS="/opt/logaudit/patterns/known-errors.txt"
OUTPUT="/opt/logaudit/output/report.txt"

grep -f "$PATTERNS" "$LOGDIR/api-server.log" | sort | uniq -c | sort -n > "$OUTPUT"
