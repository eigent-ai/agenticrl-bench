#!/bin/bash
set -e
mkdir -p /opt/warehouse/reports
cd /opt/warehouse
sqlite3 tracking.db < schema.sql
sqlite3 tracking.db < seed_data.sql
