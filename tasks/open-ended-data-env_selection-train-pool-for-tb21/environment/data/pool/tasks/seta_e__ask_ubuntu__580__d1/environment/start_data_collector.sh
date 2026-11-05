#!/bin/bash
nohup python3 /app/services/data_collector.py > /var/log/data_collector.log 2>&1 &
echo $!
