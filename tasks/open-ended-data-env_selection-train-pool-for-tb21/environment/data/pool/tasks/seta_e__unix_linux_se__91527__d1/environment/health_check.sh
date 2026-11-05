#!/bin/bash
# Reports the number of healthy worker processes.
# Exits 0 if all configured workers are healthy, 1 otherwise.

PID_DIR="/var/run/workerd"
WORKERS=3
healthy=0

for i in $(seq 1 $WORKERS); do
    pid_file="$PID_DIR/worker_${i}.pid"
    if [ -f "$pid_file" ]; then
        pid=$(cat "$pid_file")
        if pgrep -x "worker.py" | grep -qx "$pid"; then
            ((healthy++))
        fi
    fi
done

echo "healthy_workers=${healthy}"
[ "$healthy" -eq "$WORKERS" ]
