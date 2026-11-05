#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') $@" >> /var/log/apparmor_parser_calls.log
exec /usr/sbin/apparmor_parser.real "$@" 2>/dev/null || true
