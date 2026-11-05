#!/bin/bash
# CPU stress worker - performs intensive arithmetic
while true; do
    i=0
    while [ $i -lt 500000 ]; do
        i=$((i + 1))
    done
done
