#!/bin/bash

LOG=/var/log/primon/alerts.log

current_hour=$(date +'%H')

if [ "$current_hour" -ge "8" ] && [ "$current_hour" -le "18" ]; then
    non_default_priorities="$(ps -eo pid,comm,nice,uid --sort nice | awk '$3 != 0')"

    if [ -n "$non_default_priorities" ]; then
        echo "Processes with non-default CPU scheduling priority: $non_default_priorities" | mail -s "Root Non-default CPU Priority Alert" root@localhost
    fi
fi
