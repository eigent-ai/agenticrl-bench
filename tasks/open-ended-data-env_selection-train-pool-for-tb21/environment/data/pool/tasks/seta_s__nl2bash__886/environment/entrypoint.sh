#!/bin/bash
# Set up the corrupted /etc/hosts at container start
if [ -f /opt/infra/.hosts_corrupted ]; then
    cat /opt/infra/.hosts_corrupted > /etc/hosts
fi
exec "$@"
