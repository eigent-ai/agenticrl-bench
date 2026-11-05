#!/bin/bash
iptables -A OUTPUT -p tcp --dport 11371 -j DROP 2>/dev/null || true
exec "$@"
