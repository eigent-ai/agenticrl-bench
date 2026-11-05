#!/bin/bash
mkdir -p /run/sshd
/usr/sbin/sshd
exec sleep infinity
