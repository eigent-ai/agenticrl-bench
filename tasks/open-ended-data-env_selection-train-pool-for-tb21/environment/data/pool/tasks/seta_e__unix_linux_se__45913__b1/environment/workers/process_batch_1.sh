#!/bin/bash
echo "Worker 1 starting"
for i in $(seq 1 5); do
    echo "Processing record $i"
done
echo "Worker 1 complete: 5 records processed"
