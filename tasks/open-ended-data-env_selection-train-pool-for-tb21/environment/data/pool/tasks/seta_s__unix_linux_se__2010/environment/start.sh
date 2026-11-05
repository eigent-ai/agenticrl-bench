#!/bin/bash
mkdir -p /run/sshd
/usr/sbin/sshd
exec tail -f /dev/null
