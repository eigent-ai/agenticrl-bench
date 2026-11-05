#!/bin/bash
rsync --daemon
/usr/sbin/sshd
exec sleep infinity
