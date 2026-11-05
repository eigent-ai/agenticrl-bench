#!/bin/bash
BASEDIR="$(cd "$(dirname "$0")" && pwd)"
RUNDIR="$BASEDIR/run"

echo "Worker Status:"
echo "=============="

for pidfile in "$RUNDIR"/*.pid; do
    [ -f "$pidfile" ] || continue
    NAME=$(basename "$pidfile" .pid)
    PID=$(cat "$pidfile")
    if [ -f "$pidfile" ]; then
        echo "$NAME (PID $PID): running"
    else
        echo "$NAME (PID $PID): stopped"
    fi
done
