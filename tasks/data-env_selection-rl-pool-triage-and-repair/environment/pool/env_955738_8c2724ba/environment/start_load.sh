#!/bin/bash
# Start the traffic generator in background with a discoverable name
nohup /opt/network-load/traffic_generator.sh > /dev/null 2>&1 &
echo $! > /tmp/traffic_generator.pid
