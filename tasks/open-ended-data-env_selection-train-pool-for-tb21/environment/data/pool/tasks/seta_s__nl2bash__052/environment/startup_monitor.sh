#!/bin/bash

startup_time_threshold=10
slow_startup_services=$(systemd-analyze blame | grep 's' | awk '{print $2}')
for service in "$slow_startup_services"; do
    service_startup_time=$(systemd-analyze blame | grep "$service" | awk '{print $1}')
    if [ "$service_startup_time" -gt "$startup_time_threshold" ]; then
        echo "Service $service takes too long to start."
    fi
done
