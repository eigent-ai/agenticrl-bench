#!/bin/bash
# filter.sh - Extract CRITICAL severity records from master CSV
# Usage: bash filter.sh <master_csv> <output_csv>

MASTER="$1"
OUTPUT="$2"

if [ -z "$MASTER" ] || [ ! -f "$MASTER" ]; then
    echo "Error: Master CSV not found: $MASTER" >&2
    exit 1
fi

grep "CRITICAL" "$MASTER" | sort -u > "$OUTPUT"
