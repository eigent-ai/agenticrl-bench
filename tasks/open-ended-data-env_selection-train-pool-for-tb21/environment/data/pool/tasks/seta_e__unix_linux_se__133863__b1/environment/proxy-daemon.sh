#!/bin/bash
# Continuously invokes HAProxy and restarts it after any exit.
# This daemon keeps the TCP proxy alive despite transient failures.
while true; do
    echo "[$(date -u +%FT%TZ)] Starting HAProxy..."
    /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -db 2>&1
    echo "[$(date -u +%FT%TZ)] HAProxy exited with code $?. Restarting in 10 seconds..."
    sleep 10
done
