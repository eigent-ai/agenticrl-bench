#!/bin/bash
if ! pgrep -x supervisord > /dev/null 2>&1; then
    mkdir -p /var/log/supervisor
    /usr/bin/supervisord -c /etc/supervisor/supervisord.conf
    sleep 3
fi
