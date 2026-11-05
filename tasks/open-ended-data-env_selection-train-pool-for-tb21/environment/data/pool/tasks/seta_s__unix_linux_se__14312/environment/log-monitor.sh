#!/bin/bash
# Monitor log files on remote servers
LOGFILE="${1:-/var/log/syslog}"
PATTERN="${2:-error}"
SERVERS="${3:-localhost}"

for server in $SERVERS; do
  ssh -p 2222 -o StrictHostKeyChecking=no "$server" \
    "tail -f $LOGFILE" | grep -i "$PATTERN" &
done
wait
