#!/bin/bash
nohup python3 /app/services/data_processor.py > /var/log/data_processor.log 2>&1 &
echo $!
