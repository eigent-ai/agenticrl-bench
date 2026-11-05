#!/bin/bash
IMG=/opt/storage/disk.img
MOUNT=/data

if [ ! -f "$IMG" ]; then
    echo "Error: Image file $IMG not found"
    exit 1
fi

mount -o loop,ro "$IMG" "$MOUNT"
if [ $? -eq 0 ]; then
    echo "Mounted $IMG at $MOUNT"
else
    echo "Failed to mount $IMG at $MOUNT"
    exit 1
fi
