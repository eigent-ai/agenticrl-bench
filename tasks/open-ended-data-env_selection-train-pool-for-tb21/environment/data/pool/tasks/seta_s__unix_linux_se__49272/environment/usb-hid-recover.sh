#!/bin/bash
set -e

LOG=/var/log/usb-hid-recover.log

echo "$(date): Starting USB HID module recovery" >> "$LOG"

modprobe -r usbhid
sleep 1
modprobe usbhid

echo "$(date): Module recovery complete" >> "$LOG"
