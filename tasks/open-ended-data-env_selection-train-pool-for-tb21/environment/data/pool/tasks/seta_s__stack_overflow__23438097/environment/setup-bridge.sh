#!/bin/bash

source /opt/netmon/config.conf

BRIDGE=$(echo $BRIDGE_NAME | xargs)
ADDR=$(echo $BRIDGE_IP | xargs)

mkdir -p /opt/netmon/state/bridges

echo "name=$BRIDGE" > /opt/netmon/state/bridges/$BRIDGE

brctl addbr $BRIDGE

if [ $? -eq 0 ]; then
    echo "ip=$ADDR" >> /opt/netmon/state/bridges/$BRIDGE
    echo "state=UP" >> /opt/netmon/state/bridges/$BRIDGE
fi
