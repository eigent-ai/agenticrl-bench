#!/bin/bash
exec su -s /bin/bash monitor -c 'setsid /opt/monitor/collect_stats.sh < /dev/null'
