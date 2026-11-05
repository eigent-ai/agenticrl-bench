#!/bin/bash
/usr/sbin/sshd
ssh-keyscan -p 2222 localhost >> /root/.ssh/known_hosts 2>/dev/null
exec "$@"
