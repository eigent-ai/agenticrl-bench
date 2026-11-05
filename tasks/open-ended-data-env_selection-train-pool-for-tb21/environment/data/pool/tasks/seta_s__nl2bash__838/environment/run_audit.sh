#!/bin/bash
# Audio export disk usage audit
CONF="/srv/audio/audit.conf"
REPORT_DIR="/srv/audio/reports"

# Read scan directory from config
SCAN_DIR=$(head -1 "$CONF")

# Find exported WAV files and calculate space
find "$SCAN_DIR" -name "export*.wav" | ./calc_space > "$REPORT_DIR/disk_usage.json"
