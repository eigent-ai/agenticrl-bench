#!/bin/bash
echo "Verifying mount configuration..."
while IFS= read -r line; do
    [[ "$line" =~ ^#.*$ ]] && continue
    [[ -z "$line" ]] && continue
    device=$(echo "$line" | awk '{print $1}')
    mountpoint=$(echo "$line" | awk '{print $2}')
    lsblk "$device" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "ERROR: Device $device not found"
        exit 1
    fi
    echo "Verified: $device -> $mountpoint"
done < /opt/diskmon/fstab.rules
echo "Mount configuration verified successfully"
