#!/bin/bash
usermod -d /var/lib/mysql/ mysql 2>/dev/null
mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld
mysqld_safe &
for i in $(seq 1 30); do
    if mysqladmin ping --silent 2>/dev/null; then
        break
    fi
    sleep 1
done
exec sleep infinity
