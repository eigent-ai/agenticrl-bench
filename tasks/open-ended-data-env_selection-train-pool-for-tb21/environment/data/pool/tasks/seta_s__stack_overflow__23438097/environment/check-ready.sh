#!/bin/bash

source /opt/netmon/config.conf

BRIDGE=$(echo $BRIDGE_NAME | xargs)
MAX=$(echo $MAX_WAIT)

STATEFILE=/opt/netmon/state/bridges/$BRIDGE

i=0
while [ $i -lt $MAX ]; do
    ping -c1 -W1 10.99.0.1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Bridge $BRIDGE is ready."
        exit 0
    fi
    sleep 1
    i=$((i+1))
done

echo "Bridge $BRIDGE did not become ready within $MAX seconds."
exit 1
