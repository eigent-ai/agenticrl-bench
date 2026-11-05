#!/bin/bash
# Build Freshness Audit
# Finds the most recently modified file in each project

PROJECTS_DIR="/opt/builds/projects"
echo "project,latest_file,mtime_epoch"

for project_dir in "$PROJECTS_DIR"/*/; do
    name=$(basename "$project_dir")
    latest=$(find -L "$project_dir" -type f | xargs ls -drt 2>/dev/null | tail -n 1)
    if [ -n "$latest" ]; then
        ts=$(stat -c '%Y' "$latest" 2>/dev/null)
        echo "$name,$latest,$ts"
    fi
done
