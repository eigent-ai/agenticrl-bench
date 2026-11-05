#!/bin/bash
BASEDIR="$(dirname "$(readlink -f "$0")")/.."
source "$BASEDIR/config/env.sh"
CONF_DIR="${DISKMON_CONFIG:-$BASEDIR/config}"
OUTPUT="$DISKMON_DATA/collect_raw.csv"

> "$OUTPUT"

while IFS= read -r mount; do
    mount=$(echo "$mount" | xargs)
    if mountpoint -q "$mount" 2>/dev/null; then
        info=$(df -h "$mount" | tail -1 | awk '{print $1" "$2" "$3" "$3" "$5}')
        echo "$info" >> "$OUTPUT"
    fi
done < "$CONF_DIR/monitors.conf"
