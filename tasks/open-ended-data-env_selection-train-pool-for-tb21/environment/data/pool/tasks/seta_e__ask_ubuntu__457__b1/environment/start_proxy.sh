#!/bin/bash
# Start tinyproxy daemon with restrictive configuration
mkdir -p /var/log/tinyproxy
chown tinyproxy:tinyproxy /var/log/tinyproxy
tinyproxy -c /etc/tinyproxy/tinyproxy.conf
exec "$@"
