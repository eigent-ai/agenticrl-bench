#!/bin/bash
while true; do
    if ! pgrep -f "/usr/local/bin/snap-store" > /dev/null 2>&1; then
        nohup /usr/local/bin/snap-store > /dev/null 2>&1 &
    fi
    sleep 3
done
