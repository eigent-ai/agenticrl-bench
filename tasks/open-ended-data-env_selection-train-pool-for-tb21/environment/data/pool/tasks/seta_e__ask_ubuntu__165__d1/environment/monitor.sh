#!/bin/bash
# Simple monitoring script
echo "System check at $(date)"
df -h / | tail -1 | awk '{print "Disk usage: " $5}'
echo "Monitor check complete"
