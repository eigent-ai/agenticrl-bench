#!/bin/bash
# Select K unique random files from the server list
# Usage: select_files.sh <count>

COUNT=$1
BASEDIR="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$BASEDIR/config/servers.list"

# Read server list
SERVERS=()
while IFS= read -r line; do
    # Strip inline comments
    line="${line%%#*}"
    SERVERS+=("$line")
done < "$CONFIG"

TOTAL=${#SERVERS[@]}

if [ "$COUNT" -gt "$TOTAL" ]; then
    echo "Error: requested $COUNT files but only $TOTAL available" >&2
    exit 1
fi

# Select random files
for ((i=0; i<COUNT; i++)); do
    IDX=$("$BASEDIR/bin/random_range.sh" "$TOTAL")
    echo "${SERVERS[$((IDX-1))]}"
done
