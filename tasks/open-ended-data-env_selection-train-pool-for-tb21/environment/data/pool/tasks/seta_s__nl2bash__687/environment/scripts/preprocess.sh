#!/bin/bash
set -e
cd "$(dirname "$0")/.."
# Concatenate all CSV input files, skip headers on subsequent files
first=1
for f in data/input/*.csv; do
    if [ "$first" -eq 1 ]; then
        cat "$f"
        first=0
    else
        tail -n +2 "$f"
    fi
done > data/output/combined.csv
# Also copy text notes
cat "data/input/summary & notes.txt" > data/output/notes.txt
echo "Preprocessing complete: $(wc -l < data/output/combined.csv) lines"
