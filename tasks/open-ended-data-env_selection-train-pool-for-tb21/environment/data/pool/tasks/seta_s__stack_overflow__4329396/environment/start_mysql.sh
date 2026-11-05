#!/bin/bash
if ! mysqladmin ping --silent 2>/dev/null; then
    mkdir -p /var/run/mysqld
    chown mysql:mysql /var/run/mysqld
    mysqld --user=mysql --daemonize
    for i in $(seq 1 30); do
        if mysqladmin ping --silent 2>/dev/null; then
            break
        fi
        sleep 1
    done
fi
