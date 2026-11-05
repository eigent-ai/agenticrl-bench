#!/bin/bash
#
# Build orchestrator — runs four stages sequentially,
# logging each stage's output to its own log file while
# printing status lines to the terminal.
#

set -e

BASEDIR="$(cd "$(dirname "$0")" && pwd)"
LOGDIR="$BASEDIR/logs"

mkdir -p "$LOGDIR"

# Save original stdout so we can print status to terminal
exec 3>&1

echo "=== Build Pipeline Starting ===" >&3

for i in 1 2 3 4; do
    LOGFILE="$LOGDIR/stage${i}.log"
    echo "[status] Stage $i: starting" >&3

    # Redirect stdout to the stage log file
    exec 1>>"$LOGFILE"

    # Run the stage script
    source "$BASEDIR/stages/stage${i}.sh"

    echo "[status] Stage $i: completed" >&3
done

echo "=== All stages completed ===" >&3

# Restore stdout/stderr for merge step
exec 1>&3 3>&-

echo "Running log merge..."
bash "$BASEDIR/merge_logs.sh"

echo "=== Build Pipeline Finished ==="
exit 0
