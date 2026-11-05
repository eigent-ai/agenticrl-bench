#!/bin/bash

source /opt/netmon/config.conf

BRIDGE=$(echo $BRIDGE_NAME | xargs)
STATEDIR=/opt/netmon/state

mkdir -p $STATEDIR/interfaces

for i in 1 2 3; do
    cat > $STATEDIR/interfaces/veth-host${i} << EOF
name=veth-host${i}
type=veth
peer=veth-cont${i}
master=$BRIDGE
state=UP
EOF
    sleep 1
done

echo "Created 3 veth pair configurations attached to $BRIDGE"
