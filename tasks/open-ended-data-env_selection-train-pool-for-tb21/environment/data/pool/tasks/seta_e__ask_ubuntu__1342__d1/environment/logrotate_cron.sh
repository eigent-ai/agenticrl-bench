#!/bin/sh

# Clean up logrotate state file if it exists and is empty
test -s /var/lib/logrotate/status || rm -f /var/lib/logrotate/status

/usr/sbin/logrotate /etc/logrotate.conf
