#!/bin/bash
set -e
service postgresql start
sleep 4
su -c "psql -c \"CREATE USER analyst WITH SUPERUSER;\"" postgres
su -c "psql -c \"CREATE DATABASE reporting OWNER analyst;\"" postgres
su -c "psql -d reporting -f /tmp/init.sql" postgres
