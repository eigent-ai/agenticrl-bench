#!/bin/bash
# Code Audit Tool - Generates per-project line count metrics
# Usage: ./code_audit.sh

PROJECTS_DIR="/opt/projects"
REPORT_FILE="/opt/reports/code_audit.csv"

echo "project,file_count,total_lines" > "$REPORT_FILE"

total_files=0
total_lines=0

for project_dir in "$PROJECTS_DIR"/*/; do
    project_name=$(basename "$project_dir")

    # Count C source files and their lines
    file_count=$(find "$project_dir" -name "*.c" | wc -l)
    line_count=$(find "$project_dir" -name "*.c" | xargs cat 2>/dev/null | wc -l)

    echo "$project_name,$file_count,$line_count" >> "$REPORT_FILE"

    total_files=$((total_files + file_count))
    total_lines=$((total_lines + line_count))
done

echo "TOTAL,$total_files,$total_lines" >> "$REPORT_FILE"

echo "Audit complete. Report written to $REPORT_FILE"
