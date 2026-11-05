#!/bin/bash
# Compare value $1 against warning threshold $2 and critical threshold $3
# Returns: OK, WARNING, or CRITICAL
value="$1"
warn="$2"
crit="$3"

if [[ "$value" > "$crit" ]]; then
    echo "CRITICAL"
elif [[ "$value" > "$warn" ]]; then
    echo "WARNING"
else
    echo "OK"
fi
