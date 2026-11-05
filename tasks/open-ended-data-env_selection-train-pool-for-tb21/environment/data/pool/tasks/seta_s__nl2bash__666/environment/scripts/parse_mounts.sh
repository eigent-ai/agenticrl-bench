#!/bin/bash
# Parse NFS mount points from a server snapshot file

SNAPSHOT_FILE="$1"

if [ -z "$SNAPSHOT_FILE" ]; then
    echo "Usage: parse_mounts.sh <snapshot_file>" >&2
    exit 1
fi

if [ ! -f "$SNAPSHOT_FILE" ]; then
    echo "Error: Snapshot file not found: $SNAPSHOT_FILE" >&2
    exit 1
fi

# Extract NFS mount lines and their mount points
grep 'type nfs ' "$SNAPSHOT_FILE" | sed 's/.* on \(.*\) (.*/\1/'
