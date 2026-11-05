#!/bin/bash
# Process Compliance Audit Tool v2.1
# Scans running processes and classifies binaries against approved directories

CONFIG_FILE="/etc/compliance/approved_dirs.conf"
REPORT_FILE="/var/reports/process_audit.json"

mkdir -p "$(dirname "$REPORT_FILE")"

# Collect binary paths from running processes
ps aux | awk '{print $1}' | grep -x -e "/.*" | sort -u | while read binary; do
    dir=$(dirname "$binary")
    if grep -qx "$dir" "$CONFIG_FILE"; then
        status="compliant"
    else
        status="non_compliant"
    fi
    echo "$binary,$dir,$status"
done > "$REPORT_FILE"

echo "Audit complete. Report saved to $REPORT_FILE"
