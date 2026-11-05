#!/bin/bash
# Data Retention Audit Tool
# Finds the oldest regular file in each project directory
# Output: CSV report with project, file path, modification date

PROJECTS_DIR="/srv/projects"
OUTPUT="/srv/reports/audit.csv"

mkdir -p "$(dirname "$OUTPUT")"
echo "project,oldest_file,mod_date" > "$OUTPUT"

for project in "$PROJECTS_DIR"/*/; do
    pname=$(basename "$project")
    # Find oldest regular file in project (excluding hidden files for cleanliness)
    oldest=$(find -L "$project" -type f -not -name '.*' -print | xargs ls -ltr 2>/dev/null | head -n 1 | awk '{print $NF}')
    if [ -n "$oldest" ]; then
        mod_date=$(stat -c '%y' "$oldest" 2>/dev/null | cut -d' ' -f1)
        echo "$pname,$oldest,$mod_date" >> "$OUTPUT"
    fi
done

echo "Audit complete. Report saved to $OUTPUT"
