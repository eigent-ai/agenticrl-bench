#!/bin/bash
mkdir -p /var/run/procmon
echo $$ > /var/run/procmon/coordinator.pid

for i in 1 2 3; do
    /opt/procmon/worker.sh "$i" &
done

wait
