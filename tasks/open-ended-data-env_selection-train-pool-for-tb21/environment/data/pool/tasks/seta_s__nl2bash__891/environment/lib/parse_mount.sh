#!/bin/bash
# Parse mount output into structured pipe-delimited format
# Usage: parse_mount.sh <snapshot_file>
# Output: device|mountpoint|fstype|options (one per line)

SNAPSHOT_FILE="$1"

if [ ! -f "$SNAPSHOT_FILE" ]; then
    echo "Error: Snapshot file not found: $SNAPSHOT_FILE" >&2
    exit 1
fi

grep -E '^/' "$SNAPSHOT_FILE" | \
sed -n 's/^\(.*\) on \(.*\) type \(.*\) (\(.*\))$/\1|\2|\3|\4/p'
