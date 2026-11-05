#!/bin/bash
# Generate command frequency report from bash history

HIST_FILE="${HOME}/.bash_history"

if [ ! -r "$HIST_FILE" ]; then
    echo "ERROR: Cannot read history file: $HIST_FILE" >&2
    exit 1
fi

if [ ! -s "$HIST_FILE" ]; then
    echo "ERROR: History file is empty: $HIST_FILE" >&2
    exit 1
fi

echo "=== Command Frequency Report ==="
echo "History file: $HIST_FILE"
echo "Total commands: $(wc -l < "$HIST_FILE")"
echo ""
echo "Top 10 commands:"
awk '{print $1}' "$HIST_FILE" | sort | uniq -c | sort -rn | head -10
echo ""
echo "Report generated: $(date)"
