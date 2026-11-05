#!/bin/bash
# Format audit discrepancies into a report

# Print header
echo "Server,Mount Point,Status"

# Format each discrepancy line
while IFS='|' read -r server mount status; do
    [ -z "$server" ] && continue
    echo "${server},${mount},${status}"
done
