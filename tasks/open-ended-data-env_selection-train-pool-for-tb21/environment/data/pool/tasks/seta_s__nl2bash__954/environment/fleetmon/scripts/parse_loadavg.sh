#!/bin/bash
# Parse load averages from a server's proc_loadavg snapshot
SNAPSHOT_DIR="$1"
awk '{print $1, $3, $4}' "$SNAPSHOT_DIR/proc_loadavg"
