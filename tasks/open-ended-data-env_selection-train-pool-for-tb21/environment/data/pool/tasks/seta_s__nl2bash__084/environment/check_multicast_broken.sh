#!/bin/bash

pcap_file="$1"
threshold="$2"

multicast_packets=$(tcpdump -r "$pcap_file" multicast 2>/dev/null | grep 'packets captured' | awk '{print $3}')

if [ "$multicast_packets" = "$threshold" ]; then
    echo "ALERT: $multicast_packets packets exceeded threshold"
fi
