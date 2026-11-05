#!/bin/bash
# Finger audit wrapper - logs all user lookups for compliance
echo "$(date '+%Y-%m-%d %H:%M:%S'): finger lookup for $*" >> /var/log/finger_audit.log
exec /usr/bin/finger -s "$@"
