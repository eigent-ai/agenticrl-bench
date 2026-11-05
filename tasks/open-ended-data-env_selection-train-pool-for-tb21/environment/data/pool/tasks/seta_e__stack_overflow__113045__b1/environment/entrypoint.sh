#!/bin/bash
# Start PostgreSQL and then execute the provided command
service postgresql start
exec "$@"
