#!/bin/bash
set -euo pipefail

CONFIG="$HOME/.monitor_config"
if [[ ! -f "$CONFIG" ]]; then
    echo "ERROR: Configuration file not found: $CONFIG" >&2
    exit 1
fi
source "$CONFIG"

LOAD=$(syscheck --load)
DISK=$(syscheck --disk)

{
    echo "=== System Health Report ==="
    echo "Generated: $(date -Iseconds)"
    echo "Load Average: $LOAD"
    echo "Disk Usage: $DISK"
    echo "WARN_THRESHOLD=${WARN_THRESHOLD}"
    echo "CRIT_THRESHOLD=${CRIT_THRESHOLD}"
} > "${REPORT_PATH}"

echo "Health report written to: ${REPORT_PATH}"
