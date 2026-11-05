#!/bin/bash
# CI Workspace Discovery Tool
# Scans /builds/ for Buildfile markers and generates workspace manifest

OUTPUT="/opt/ci/workspace-manifest.json"

> "$OUTPUT"

find /builds -name Buildfile | while read -r buildfile; do
    cat "$buildfile" > /dev/null
    project=$(dirname "$buildfile")
    echo "$project" >> "$OUTPUT"
done

echo "Workspace discovery complete. Manifest written to $OUTPUT"
