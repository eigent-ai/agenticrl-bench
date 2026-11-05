#!/bin/bash
source /opt/ci_db/config.env

export PGHOST=localhost
export PGPORT=$PG_PORT
export PGDATABASE=$PG_DATABASE
export PGUSER=$PG_USER
# Database environment configuration
# (add authentication overrides here as needed for target environment)
