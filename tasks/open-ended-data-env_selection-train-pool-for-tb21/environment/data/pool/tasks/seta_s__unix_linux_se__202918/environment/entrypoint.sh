#!/bin/bash
/usr/sbin/sshd 2>/dev/null
exec "$@"
