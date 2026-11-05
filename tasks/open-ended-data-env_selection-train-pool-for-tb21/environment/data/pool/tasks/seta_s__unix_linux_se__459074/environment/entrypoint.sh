#!/bin/bash
mkdir -p /run/sshd
ssh-keygen -A -q
/usr/sbin/sshd
exec "$@"
