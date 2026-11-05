#!/bin/bash
nohup python3 /app/services/report_generator.py > /var/log/report_generator.log 2>&1 &
echo $!
