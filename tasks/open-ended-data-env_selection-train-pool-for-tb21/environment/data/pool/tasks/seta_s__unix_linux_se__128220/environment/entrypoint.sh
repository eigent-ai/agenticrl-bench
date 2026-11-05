#!/bin/bash
echo "nameserver 127.0.1.1" > /etc/resolv.conf
mkdir -p /run/resolvconf
echo "nameserver 127.0.1.1" > /run/resolvconf/resolv.conf
exec "$@"
