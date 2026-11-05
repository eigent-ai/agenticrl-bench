#!/bin/bash

INDEX_FILE="/opt/services/indexer/file_index.txt"
> "$INDEX_FILE"

for f in /var/log/*.log; do
    if [ -f "$f" ]; then
        SIZE=$(dd if="$f" bs=1 of=/dev/null 2>&1 | grep -o '[0-9]* bytes' | awk '{print $1}')
        echo "$f $SIZE" >> "$INDEX_FILE"
    fi
done
