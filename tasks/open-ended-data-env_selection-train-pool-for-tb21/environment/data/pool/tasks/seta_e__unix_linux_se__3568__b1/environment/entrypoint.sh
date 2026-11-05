#!/bin/bash
mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
service mysql start 2>/dev/null || mysqld_safe --skip-syslog &
sleep 3
exec "$@"
