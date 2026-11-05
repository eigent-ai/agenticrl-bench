#!/bin/bash
# Parse lsblk capture and classify devices by driver using proc_devices

source /opt/hwaudit/config.sh

LSBLK_FILE="${DATA_DIR}/lsblk_capture.txt"
PROCDEV_FILE="${DATA_DIR}/proc_devices.txt"

declare -A driver_map
# Build driver map from proc_devices
while IFS= read -r line; do
    major=$(echo "$line" | awk '{print $1}')
    name=$(echo "$line" | awk '{print $2}')
    if [[ "$major" =~ ^[0-9]+$ ]]; then
        driver_map[$major]="$name"
    fi
done < "$PROCDEV_FILE"

# Parse lsblk output
devices="[]"
first=true

cat "$LSBLK_FILE" | grep -v "^NAME" | grep -v "^[├└│]" | while read -r line; do
    name=$(echo "$line" | awk '{print $1}')
    majmin=$(echo "$line" | awk '{print $2}')
    dev_type=$(echo "$line" | awk '{print $6}')

    # Extract major and minor
    major=$(echo "$majmin" | cut -d':' -f1)
    minor=$(echo "$majmin" | cut -d':' -f2)

    driver="${driver_map[$major]:-unknown}"

    if [ "$first" = true ]; then
        devices="[{\"name\":\"${name}\",\"major\":${major},\"minor\":${minor},\"type\":\"${dev_type}\",\"driver\":\"${driver}\"}"
        first=false
    else
        devices="${devices},{\"name\":\"${name}\",\"major\":${major},\"minor\":${minor},\"type\":\"${dev_type}\",\"driver\":\"${driver}\"}"
    fi
done

devices="${devices}]"
echo "$devices"
