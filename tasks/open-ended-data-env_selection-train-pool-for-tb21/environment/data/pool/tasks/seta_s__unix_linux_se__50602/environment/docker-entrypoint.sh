#!/bin/bash
NETSTATE="/var/lib/netstate"
mkdir -p "${NETSTATE}/net1"

echo "10.10.0.1/24" > "${NETSTATE}/net1/addr"
echo "up"            > "${NETSTATE}/net1/link"
echo "default via 10.10.0.254 dev net1 metric 500" > "${NETSTATE}/net1/route"

mkdir -p /run/network
printf 'lo=lo\n' > /run/network/ifstate

exec "$@"
