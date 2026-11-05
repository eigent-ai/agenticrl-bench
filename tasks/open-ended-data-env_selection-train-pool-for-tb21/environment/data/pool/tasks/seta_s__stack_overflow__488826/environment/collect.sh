#!/bin/bash

OUTPUT="/var/log/collected_errors.txt"

while true; do
    find / -type f -exec grep -H 'ERROR' {} \; > "$OUTPUT" 2>/dev/null
    sleep 120
done
