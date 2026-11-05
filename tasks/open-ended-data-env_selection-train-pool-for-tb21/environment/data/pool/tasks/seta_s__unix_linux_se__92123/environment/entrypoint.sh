#!/bin/bash
/usr/sbin/sshd -e
exec tail -f /dev/null
