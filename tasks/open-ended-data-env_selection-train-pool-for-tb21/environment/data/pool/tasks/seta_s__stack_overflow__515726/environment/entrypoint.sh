#!/bin/bash
mkdir -p /run/sshd
# Ensure .ssh directory permissions are correct for sshd auth
chmod 0700 /home/syncuser/.ssh
/usr/sbin/sshd
exec "$@"
