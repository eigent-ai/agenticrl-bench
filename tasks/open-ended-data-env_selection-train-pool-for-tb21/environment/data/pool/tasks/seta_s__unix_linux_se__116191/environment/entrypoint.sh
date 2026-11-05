#!/bin/bash

mkdir -p /run/sshd

# Start bastion sshd with debug logging to a file
/usr/sbin/sshd -f /etc/ssh/sshd_config_bastion -E /var/log/bastion_sshd.log

python3 /opt/services/registry_server.py &
python3 /opt/services/api_server.py &

iptables -A OUTPUT -p tcp --dport 9091 -m owner --uid-owner 1000 -j REJECT 2>/dev/null || true
iptables -A OUTPUT -p tcp --dport 9200 -m owner --uid-owner 1000 -j REJECT 2>/dev/null || true

sleep 1

exec "$@"
