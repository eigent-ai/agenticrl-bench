#!/bin/bash
cd /opt/log-aggregator
nohup python3 /opt/log-aggregator/log_aggregator.py > /dev/null 2>&1 &
echo "Log aggregator started with PID $!"
