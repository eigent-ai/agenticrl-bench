#!/bin/bash
mkdir -p /run/sshd
/usr/sbin/sshd
python3 -m http.server 8888 --directory /tmp &>/dev/null &
exec sleep infinity
