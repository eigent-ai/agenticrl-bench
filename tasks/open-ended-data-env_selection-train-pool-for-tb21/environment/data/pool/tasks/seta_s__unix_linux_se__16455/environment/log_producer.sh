#!/bin/bash

FIFO_PATH="/opt/logpipe/data.fifo"
TOTAL_RECORDS=5000

for i in $(seq 1 $TOTAL_RECORDS); do
    SEQ=$(printf "%05d" "$i")
    TIMESTAMP=$(date +%s)
    PAYLOAD=$(head -c 100 /dev/urandom | od -An -tx1 | tr -d ' \n' | head -c 200)
    echo "RECORD:${SEQ}:${TIMESTAMP}:${PAYLOAD}"
done > "$FIFO_PATH"
