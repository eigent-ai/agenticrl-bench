#!/bin/bash
echo "Loading firewall rules..."
iptables-restore < /opt/netmon/firewall.rules
if [ $? -eq 0 ]; then
    echo "Firewall rules loaded successfully"
else
    echo "ERROR: Failed to load firewall rules"
    exit 1
fi
