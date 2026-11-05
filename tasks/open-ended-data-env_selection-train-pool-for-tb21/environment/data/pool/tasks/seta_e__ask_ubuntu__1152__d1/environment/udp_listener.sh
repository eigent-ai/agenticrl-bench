#!/bin/bash
# Simple UDP listener on port 9999
while true; do
    nc -u -l -p 9999 > /dev/null 2>&1
done
