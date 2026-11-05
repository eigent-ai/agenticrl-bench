#!/bin/bash
# Process monitor - samples CPU and memory usage from /proc
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONF_FILE="$SCRIPT_DIR/procmon.conf"
LOG_DIR="$SCRIPT_DIR/logs"

mkdir -p "$LOG_DIR"

# Read configuration
INTERVAL=$(grep '^interval=' "$CONF_FILE" | cut -d= -f2)
mapfile -t PROC_LIST < <(grep '^process=' "$CONF_FILE" | cut -d= -f2)

DURATION=${1:-30}
END_TIME=$(($(date +%s) + DURATION))

while [ $(date +%s) -lt $END_TIME ]; do
    SYS_UPTIME=$(awk '{print $1}' /proc/uptime)

    for PROC_NAME in "${PROC_LIST[@]}"; do
        PIDS=$(pgrep -f "$PROC_NAME" 2>/dev/null)
        for PID in $PIDS; do
            [ ! -d "/proc/$PID" ] && continue

            STAT_LINE=$(cat /proc/$PID/stat 2>/dev/null) || continue
            UTIME=$(echo "$STAT_LINE" | cut -d' ' -f14)
            STIME=$(echo "$STAT_LINE" | cut -d' ' -f15)

            CPU_PCT=$(echo "scale=2; ($UTIME + $STIME) / $SYS_UPTIME * 100" | bc 2>/dev/null)
            [ -z "$CPU_PCT" ] && CPU_PCT=0

            MEM_KB=$(grep 'VmRss:' /proc/$PID/status 2>/dev/null | awk '{print $2}')
            [ -z "$MEM_KB" ] && MEM_KB=0

            TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
            echo "$TIMESTAMP,$PID,$PROC_NAME,$CPU_PCT,$MEM_KB" >> "$LOG_DIR/${PROC_NAME}.csv"
        done
    done
    sleep "$INTERVAL"
done
