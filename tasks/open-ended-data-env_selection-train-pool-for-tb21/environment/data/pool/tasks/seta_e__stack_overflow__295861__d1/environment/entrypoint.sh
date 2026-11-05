#!/bin/bash
mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld

echo 8 > /proc/sys/fs/inotify/max_user_watches 2>&1 || true

mysqld_safe &
sleep 3

apachectl start

exec "$@"
