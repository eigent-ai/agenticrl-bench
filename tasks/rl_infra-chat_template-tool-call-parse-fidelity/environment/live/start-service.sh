#!/bin/bash
# Start-up check of the agent box (root, before the agent starts): the live service runs (started here if needed).
set -u
[ "$(id -u)" = 0 ] || exit 1
/usr/local/bin/python3 -I /opt/live/ctl.py --ping > /dev/null 2>&1 && exit 0
install -d -m 0700 /var/log/agentrl-live /var/lib/agentrl-live /opt/live/state
cd /; umask 077
setsid /usr/local/bin/python3 -I /opt/live/liveserver.py >> /var/log/agentrl-live/service.log 2>&1 < /dev/null &
for _ in $(seq 1 30); do
  /usr/local/bin/python3 -I /opt/live/ctl.py --ping > /dev/null 2>&1 && exit 0
  sleep 1
done
exit 1
