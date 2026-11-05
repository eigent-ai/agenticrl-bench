#!/bin/bash
# Check filesystem usage against thresholds and generate alerts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.ini"

> "$ALERT_FILE"

if [ ! -f "$REPORT_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Report file not found" >> "$LOG_FILE"
    exit 1
fi

# Extract filesystem entries from JSON report
grep -oP '\{[^}]+\}' "$REPORT_FILE" | while IFS= read -r entry; do
    mount=$(echo "$entry" | grep -oP '"mount":\s*"\K[^"]*')
    use_pct=$(echo "$entry" | grep -oP '"use_pct":\s*\K[0-9]+')

    [ -z "$mount" ] || [ -z "$use_pct" ] && continue

    # Look up per-filesystem threshold, fall back to default
    sanitized=$(echo "$mount" | tr '/' '_' | sed 's/^_//')
    threshold_var="THRESHOLD_${sanitized}"
    threshold=${!threshold_var:-$DEFAULT_THRESHOLD}

    if [ "$use_pct" -gt "$threshold" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $mount at ${use_pct}% exceeds threshold ${threshold}%" >> "$ALERT_FILE"
    fi
done

alert_count=$(wc -l < "$ALERT_FILE")
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Alert check complete: $alert_count alert(s)" >> "$LOG_FILE"
