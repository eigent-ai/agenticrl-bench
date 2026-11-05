#!/bin/bash

# source /opt/monitor/config.env
threshold="10"

failed_logins=$(tail -f /var/log/auth.log | grep "password" | awk 'END{print NR}')

if [ "$failed_logins" -gt "$threshold" ]; then
    wall "ALERT: High number of failed SSH logins detected: $failed_logins"
fi
