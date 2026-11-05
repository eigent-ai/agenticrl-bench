#!/bin/bash
set -e
BASEDIR="$(dirname "$(readlink -f "$0")")/.."
LOCKFILE="$BASEDIR/run/monitor.pid"

# Check lock
if [ -f "$LOCKFILE" ]; then
    PID=$(cat "$LOCKFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "ERROR: Monitor already running (PID $PID)" >&2
        exit 1
    fi
    echo "ERROR: Lock file exists (PID $PID)" >&2
    exit 1
fi

echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

# Load environment
source "$BASEDIR/config/env.sh"

# Verify config variable
if [ -z "$DISKMON_CONFIG" ]; then
    echo "ERROR: DISKMON_CONFIG not set" >&2
    exit 1
fi

# Run pipeline
echo "Starting disk space collection..."
"$BASEDIR/bin/collect.sh"
echo "Generating report..."
"$BASEDIR/bin/report.sh"
echo "Checking thresholds..."
"$BASEDIR/bin/alert.sh"
echo "Updating history..."
"$BASEDIR/bin/history.sh"
echo "Monitor complete."
