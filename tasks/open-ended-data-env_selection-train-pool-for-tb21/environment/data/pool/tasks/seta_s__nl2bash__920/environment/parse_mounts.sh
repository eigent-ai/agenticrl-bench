#!/bin/bash
# Parse mount output into pipe-delimited format: device|mountpoint|fstype|options
# Usage: parse_mounts.sh <mount_output_file>

input_file="$1"

if [ ! -f "$input_file" ]; then
    echo "Error: File not found: $input_file" >&2
    exit 1
fi

# Parse each line of mount output format: device on /path type fstype (options)
while read line; do
    device=$(echo $line | awk '{print $1}')
    mountpoint=$(echo $line | sed -e "s/^[^/]*\ type .*$/\1/g")
    fstype=$(echo $line | awk '{print $5}')
    options=$(echo $line | grep -o '(.*)' | tr -d '()')
    echo "$device|$mountpoint|$fstype|$options"
done < "$input_file"
