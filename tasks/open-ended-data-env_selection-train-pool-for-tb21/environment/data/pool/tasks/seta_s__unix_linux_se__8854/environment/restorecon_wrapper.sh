#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') $@" >> /var/log/restorecon_calls.log
exec /usr/sbin/restorecon "$@"
