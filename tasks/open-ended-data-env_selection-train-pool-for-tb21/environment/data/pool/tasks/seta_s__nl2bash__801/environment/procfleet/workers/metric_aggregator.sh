#!/bin/bash
LOGFILE="/opt/procfleet/logs/metric_aggregator_$$.log"
echo "metric_aggregator started with PID $$" >> "$LOGFILE"

trap 'echo "metric_aggregator $$ shutting down" >> "$LOGFILE"; exit 0' TERM

while true; do
    echo "$(date): metric_aggregator $$ aggregating metrics" >> "$LOGFILE"
    sleep 4
done
