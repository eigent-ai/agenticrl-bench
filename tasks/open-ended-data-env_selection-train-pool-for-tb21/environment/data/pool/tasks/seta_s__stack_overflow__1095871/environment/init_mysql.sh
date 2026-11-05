#!/bin/bash
set -e

mkdir -p /var/run/mysqld
chown mysql:mysql /var/run/mysqld

service mysql start

for i in $(seq 1 15); do
    if mysqladmin ping --silent 2>/dev/null; then
        break
    fi
    sleep 1
done

mysql -u root <<'EOSQL'
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'rootpass';
FLUSH PRIVILEGES;
EOSQL

mysql -u root -prootpass < /tmp/setup_mysql.sql

service mysql stop
sleep 2
