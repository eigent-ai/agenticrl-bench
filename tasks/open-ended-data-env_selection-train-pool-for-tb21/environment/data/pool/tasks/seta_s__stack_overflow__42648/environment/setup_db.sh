#!/bin/bash
set -e

pg_ctlcluster 16 main start

su - postgres -c "psql -c \"CREATE USER pipeline WITH SUPERUSER PASSWORD 'pipeline';\""
su - postgres -c "psql -c \"CREATE DATABASE orders_db OWNER pipeline;\""

psql -U pipeline -d orders_db -f /opt/pipeline/schema.sql

pg_ctlcluster 16 main stop
