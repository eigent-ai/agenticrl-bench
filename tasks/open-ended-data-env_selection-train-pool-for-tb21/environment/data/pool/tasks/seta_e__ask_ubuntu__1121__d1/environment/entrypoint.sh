#!/bin/bash
ip link add dummy0 type dummy 2>/dev/null || true
ip link set dummy0 up 2>/dev/null || true
ip addr add 10.0.0.1/24 dev dummy0 2>/dev/null || true
exec "$@"
