#!/bin/bash
# Job launcher wrapper for screen-based background processing

LOGFILE="/var/log/job-runner.log"
SPOOLDIR="/var/spool/jobs"

usage() {
    echo "Usage: $0 <job-name> <command>"
    echo "  Launches a background job in a screen session"
    exit 1
}

if [ $# -lt 2 ]; then
    usage
fi

JOBNAME="$1"
shift
COMMAND="$@"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting job: $JOBNAME" >> "$LOGFILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Command: $COMMAND" >> "$LOGFILE"

screen -S "$JOBNAME" bash -c "$COMMAND" >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Job $JOBNAME launched successfully" >> "$LOGFILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Failed to launch job $JOBNAME" >> "$LOGFILE"
fi

screen -r "$JOBNAME" >> "$LOGFILE" 2>&1
