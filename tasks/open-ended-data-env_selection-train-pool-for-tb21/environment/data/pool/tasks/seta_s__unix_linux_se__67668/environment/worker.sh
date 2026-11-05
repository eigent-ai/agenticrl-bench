#!/bin/bash
WORKER_ID=$1
for j in A B; do
    /opt/procmon/subworker.sh "${WORKER_ID}-${j}" &
done
wait
