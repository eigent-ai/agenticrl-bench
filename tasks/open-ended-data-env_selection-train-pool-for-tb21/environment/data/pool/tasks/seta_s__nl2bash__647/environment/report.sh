#!/bin/bash
# Disk Usage Audit Tool v2.1
# Generates per-project size report for /srv/projects

REPORT="/var/reports/disk-usage.txt"
PROJECTS="/srv/projects"

> "$REPORT"

for dir in $(find "$PROJECTS" -maxdepth 1 -mindepth 1 -type d); do
    size=$(du -skL "$dir" 2>/dev/null | tail -1 | cut -f1)
    name=$(basename "$dir")
    echo -e "${size}\t${name}" >> "$REPORT"
done

sort -rn -o "$REPORT" "$REPORT"

echo "Report generated at $REPORT"
