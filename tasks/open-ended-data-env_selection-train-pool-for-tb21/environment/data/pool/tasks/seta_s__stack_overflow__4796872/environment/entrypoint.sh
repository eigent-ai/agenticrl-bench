#!/bin/bash
mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
service mysql start || true
sleep 2
exec "$@"
