#!/bin/bash
# Generate daily inventory report

DATA_DIR="/opt/inventory/data"
OUTPUT="/opt/inventory/reports/latest.txt"

# Merge host, service, and load data
paste -d',' "$DATA_DIR/hosts.tsv" "$DATA_DIR/services.tsv" "$DATA_DIR/load.tsv" > /tmp/merged.tsv

# Format for tabular display
column -t /tmp/merged.tsv > /tmp/formatted.txt

# Normalize whitespace in report
sed 's/ \+/ /g' /tmp/formatted.txt > "$OUTPUT"

echo "Report generated: $OUTPUT"
