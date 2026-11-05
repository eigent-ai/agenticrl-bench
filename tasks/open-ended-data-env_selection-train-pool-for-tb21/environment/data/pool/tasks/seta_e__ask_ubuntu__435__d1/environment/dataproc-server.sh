#!/bin/bash
# Simulated forking daemon start script
PID_FILE="/var/run/dataproc.pid"
LOG_FILE="/var/log/dataproc/dataproc.log"

# Create a background process that simulates the daemon
(
    echo "started" >> "$LOG_FILE"
    while true; do
        sleep 60
    done
) &

# Save the PID
echo $! > "$PID_FILE"

exit 0
