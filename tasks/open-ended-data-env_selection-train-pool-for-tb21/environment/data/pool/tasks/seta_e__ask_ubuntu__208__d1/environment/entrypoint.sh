#!/bin/bash
# Append custom host entries to /etc/hosts at runtime
# (cannot be done during Docker build as /etc/hosts is read-only)
if [ -f /root/hosts_data ]; then
    cat /root/hosts_data >> /etc/hosts 2>/dev/null || true
fi
exec "$@"
