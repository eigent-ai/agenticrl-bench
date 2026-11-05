#!/bin/bash
BASEDIR="$(cd "$(dirname "$0")" && pwd)"
RUNDIR="$BASEDIR/run"

list_descendants() {
    local children=$(ps -o pid= --ppid "$1" 2>/dev/null)
    for pid in $children; do
        list_descendants "$pid"
    done
    echo "$children"
}

echo "Cleaning up workers..."

# Kill by walking PPID tree from launcher PID
if [ -f "$RUNDIR/launcher.pid" ]; then
    LAUNCHER_PID=$(cat "$RUNDIR/launcher.pid")
    DESCENDANTS=$(list_descendants "$LAUNCHER_PID")
    if [ -n "$DESCENDANTS" ]; then
        kill $DESCENDANTS 2>/dev/null
    fi
fi

# Also try killall as a fallback
killall worker 2>/dev/null
killall simple.sh chainer.sh daemonizer.sh 2>/dev/null

# Clean up PID files
rm -f "$RUNDIR"/*.pid

echo "Cleanup complete."
