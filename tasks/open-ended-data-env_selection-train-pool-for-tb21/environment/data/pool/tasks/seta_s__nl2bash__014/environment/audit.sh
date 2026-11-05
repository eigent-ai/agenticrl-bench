#!/bin/bash
# Audit script - checks for empty directories

for dir in $(find /opt/deployments -type d -mindepth 2); do
    count=$(ls "$dir" | wc -l)
    if [ "$count" -eq 0 ]; then
        echo "Empty: $dir"
    else
        echo "Populated: $dir"
    fi
done
