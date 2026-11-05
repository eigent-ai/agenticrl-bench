#!/bin/bash
mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
mysqld --user=mysql --daemonize --pid-file=/var/run/mysqld/mysqld.pid
sleep 3
exec "$@"
