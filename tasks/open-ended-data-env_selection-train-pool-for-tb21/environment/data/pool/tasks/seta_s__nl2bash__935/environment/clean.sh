#!/bin/bash
INPUT="$1"
OUTPUT="$2"
if [ ! -f "$INPUT" ]; then
    echo "Error: Input file not found: $INPUT" >&2
    exit 1
fi
head -1 "$INPUT" > "$OUTPUT"
tail -n +2 "$INPUT" | while read line; do
    cleaned=$(echo $line | sed 's/\\\\//g')
    # cleaned=$(echo "$cleaned" | tr -d '\r')
    echo $cleaned >> "$OUTPUT"
done
