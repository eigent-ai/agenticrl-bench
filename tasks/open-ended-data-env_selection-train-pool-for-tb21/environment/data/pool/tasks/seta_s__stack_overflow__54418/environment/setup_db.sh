#!/bin/bash
set -e

pg_ctlcluster 16 main start
sleep 2

su - postgres -c "psql -c \"CREATE USER pipeline WITH PASSWORD 'pipeline' CREATEDB;\""
su - postgres -c "psql -c \"CREATE DATABASE sales_analytics OWNER pipeline;\""

psql -U pipeline -d sales_analytics -h localhost -f /tmp/seed_data.sql

pg_ctlcluster 16 main stop
sleep 1
