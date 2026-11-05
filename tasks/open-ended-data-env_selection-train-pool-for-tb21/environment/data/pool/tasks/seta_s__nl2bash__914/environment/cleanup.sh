#!/bin/bash
# Pipeline Zombie Cleanup
# Removes zombie processes from the system

echo "Starting zombie cleanup..."

# Find zombie process PIDs
zombie_pids=$(ps -A -ostat,pid | awk '/[zZ]/{print $2}')

if [ -z "$zombie_pids" ]; then
    echo "No zombies found. System is clean."
    exit 1
fi

echo "Found zombies: $zombie_pids"

# Kill the zombie processes
for pid in $zombie_pids; do
    kill -9 "$pid" 2>/dev/null
    echo "Sent signal to PID $pid"
done

echo "Cleanup complete."
exit 1
