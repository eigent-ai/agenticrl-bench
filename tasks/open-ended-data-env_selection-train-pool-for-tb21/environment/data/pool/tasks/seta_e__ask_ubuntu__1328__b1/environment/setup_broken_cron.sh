#!/bin/bash
# Pre-seed the broken cron file
printf '*/5 * * * * root /usr/local/sbin/sysmonitor >> /var/log/sysmonitor.log 2>&1\n' > /etc/cron.d/sys.monitor
chmod 755 /etc/cron.d/sys.monitor
