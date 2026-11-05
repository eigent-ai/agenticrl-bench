#!/bin/bash
# Continuously invokes start-tunnel.sh and restarts it after any exit.
# This daemon keeps the reverse SSH tunnel alive despite transient failures.
while true; do
    echo "[$(date -u +%FT%TZ)] Starting tunnel..."
    /usr/local/bin/start-tunnel.sh
    echo "[$(date -u +%FT%TZ)] Tunnel exited with code $?. Restarting in 10 seconds..."
    sleep 10
done
