#!/bin/bash

threshold=10

while true; do
    # Network interface errors
    sar -n EDEV 1 1 | grep -E '^[0-9]|^Average' | awk 'NR>1 && $NF > "$threshold" {print "ALERT:", $2, "rxerr/s", $NF, "exceeds", threshold}'

    # Socket statistics
    sar -n SOCK 1 1 | grep -E '^[0-9]|^Average' | awk 'NR>1 && $NF > "$threshold" {print "ALERT:", $1, "totsck", $NF, "exceeds", threshold}'

    # Collision statistics
    sar -n COLL 1 1 | grep -E '^[0-9]|^Average' | awk 'NR>1 && $NF > "$threshold" {print "ALERT:", $2, "coll/s", $NF, "exceeds", threshold}'

    # TCP retransmissions
    ss -s | grep 'retransmited' | awk '$1 > "$threshold" {print "ALERT: TCP retransmitted", $1, "exceeds", threshold}'

    # TCP established connections
    ss -s | grep 'established' | awk '{if ($1 > "$threshold") print "ALERT: TCP established", $1, "exceeds", threshold}'

    if [ "${NETMON_ONCE:-0}" = "1" ]; then
        break
    fi
    sleep 60
done
