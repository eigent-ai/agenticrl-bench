#!/bin/bash
/usr/local/bin/health-monitor.sh > /dev/null 2>&1 &
exec tail -f /dev/null
