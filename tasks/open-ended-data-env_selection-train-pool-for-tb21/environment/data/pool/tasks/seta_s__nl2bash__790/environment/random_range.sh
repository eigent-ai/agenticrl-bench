#!/bin/bash
# Generate a random integer from 1 to N (inclusive)
# Usage: random_range.sh <max_value>

MAX=$1

if [ -z "$MAX" ] || [ "$MAX" -lt 1 ]; then
    echo "Usage: $0 <max>" >&2
    exit 1
fi

# Generate random number using /dev/urandom
grep -m1 -ao '[0-9]' /dev/urandom | sed s/0/10/ | head -n1
