#!/bin/bash

# source /opt/monitor/config.env
threshold="100"

broadcast_packets=$(timeout 5 tcpdump -c 100 broadcast 2>/dev/null | grep 'packets captured' | awk '{print $1}')

if [ "$broadcast_packets" -gt "$threshold" ]; then
    echo "System broadcast packets count is too high: $broadcast_packets" | mail -s "High Broadcast Packets Alert" user@example.com
fi
