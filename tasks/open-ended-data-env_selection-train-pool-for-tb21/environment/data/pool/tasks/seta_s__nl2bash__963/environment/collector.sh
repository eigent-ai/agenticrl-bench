#!/bin/bash
# Collect disk usage data and cache it
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.ini"

mkdir -p "$CACHE_DIR"

SNAPSHOT="$SCRIPT_DIR/data/df_snapshot.txt"

if [ -f "$SNAPSHOT" ]; then
    cp "$SNAPSHOT" "$CACHE_DIR/raw_df.txt"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Collected df output from snapshot" >> "$LOG_FILE"
else
    df -k > "$CACHE_DIR/raw_df.txt"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Collected df output from live system" >> "$LOG_FILE"
fi
