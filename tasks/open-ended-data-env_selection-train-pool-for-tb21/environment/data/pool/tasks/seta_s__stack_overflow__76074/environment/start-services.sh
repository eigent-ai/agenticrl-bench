#!/bin/bash

mkdir -p /run/myservices

SERVICES=("active-monitor" "legacy-api-gateway" "old-log-shipper" "dev-test-runner" "cache-warmer")

for svc in "${SERVICES[@]}"; do
    bash /usr/local/lib/myservices/${svc}.sh &
    echo $! > /run/myservices/${svc}.pid
done

exec "$@"
