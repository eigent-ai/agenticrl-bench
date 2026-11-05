#!/bin/bash
# Pipeline Zombie Monitor
# Detects zombie processes and writes report

LOGFILE="/tmp/zombie.log"

echo "=== Zombie Process Report ===" > "$LOGFILE"
echo "Timestamp: $(date)" >> "$LOGFILE"

# Find zombie processes
zombies=$(ps -ef | awk '/zombie/{print $2}')

if [ -z "$zombies" ]; then
    echo "No zombie processes found." >> "$LOGFILE"
else
    echo "Zombie PIDs: $zombies" >> "$LOGFILE"
    echo "Count: $(echo "$zombies" | wc -w)" >> "$LOGFILE"
fi

echo "Report written to $LOGFILE"
cat "$LOGFILE"
