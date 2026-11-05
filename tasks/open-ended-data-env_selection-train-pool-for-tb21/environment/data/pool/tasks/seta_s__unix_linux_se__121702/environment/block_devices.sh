#!/bin/bash

DEVICES=""
for dev in $(ls /proc/bus/block/ 2>/dev/null); do
    SIZE=$(cat /proc/bus/block/$dev/size 2>/dev/null || echo "unknown")
    DEVICES="$DEVICES$dev:$SIZE,"
done

echo "devices=$DEVICES"
