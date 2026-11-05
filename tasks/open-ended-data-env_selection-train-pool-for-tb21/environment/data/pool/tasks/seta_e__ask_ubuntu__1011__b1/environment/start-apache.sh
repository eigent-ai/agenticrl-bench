#!/bin/bash
# Start Apache if not already running
if ! pgrep -x apache2 > /dev/null 2>&1; then
    mkdir -p /var/run/apache2
    source /etc/apache2/envvars
    apachectl start 2>/dev/null || true
fi
