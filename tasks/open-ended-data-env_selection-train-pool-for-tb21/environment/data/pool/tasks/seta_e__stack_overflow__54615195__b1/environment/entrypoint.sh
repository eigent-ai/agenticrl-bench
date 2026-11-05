#!/bin/bash
mkdir -p /var/run/postgresql
chown postgres:postgres /var/run/postgresql
PG_VER=$(ls /usr/lib/postgresql/)
su - postgres -c "pg_ctlcluster $PG_VER main start"
sleep 2
exec "$@"
