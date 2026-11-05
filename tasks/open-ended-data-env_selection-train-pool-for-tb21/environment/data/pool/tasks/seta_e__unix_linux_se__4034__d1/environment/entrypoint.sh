#!/bin/bash
export TERM=xterm
mkdir -p /opt/monitor
/opt/monitor/health_check.sh &
disown $!
exec sleep infinity
