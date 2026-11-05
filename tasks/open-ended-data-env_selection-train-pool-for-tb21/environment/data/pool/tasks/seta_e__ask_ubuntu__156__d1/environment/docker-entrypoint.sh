#!/bin/bash
nohup /usr/local/bin/snap-store > /dev/null 2>&1 &
nohup /usr/local/bin/snap-store-watchdog > /dev/null 2>&1 &
sleep 2
exec "$@"
