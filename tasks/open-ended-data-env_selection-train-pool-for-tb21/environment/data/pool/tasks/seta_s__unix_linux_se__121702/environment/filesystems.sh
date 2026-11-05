#!/bin/bash

FS_LIST=""
while read -r line; do
    fs=$(echo "$line" | awk '{print $NF}')
    if [ -n "$fs" ]; then
        if [ -z "$FS_LIST" ]; then
            FS_LIST="$fs"
        else
            FS_LIST="$FS_LIST,$fs"
        fi
    fi
done < /proc/filesystems

echo "supported=$FS_LIST"
