#!/bin/bash
echo "Worker 3 starting"
for i in $(seq 1 7); do
    echo "Processing record $i"
done
echo "Worker 3 complete: 7 records processed"
