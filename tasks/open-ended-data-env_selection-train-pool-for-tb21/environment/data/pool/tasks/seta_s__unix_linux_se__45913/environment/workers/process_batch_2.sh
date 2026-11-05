#!/bin/bash
echo "Worker 2 starting"
for i in $(seq 1 3); do
    echo "Processing record $i"
done
echo "WARNING: 1 record had unexpected format" >&2
echo "Worker 2 complete: 3 records processed"
