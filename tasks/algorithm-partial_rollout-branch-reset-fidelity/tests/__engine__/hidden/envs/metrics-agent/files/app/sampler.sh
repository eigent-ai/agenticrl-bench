#!/bin/bash
# Append one sample per second to metrics.log.
while :; do
  echo "$(date +%s) $(cut -d' ' -f1 /proc/loadavg)" >> metrics.log
  sleep 1
done
