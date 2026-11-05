#!/bin/bash
pg_ctlcluster 16 main start
su - postgres -c "psql -f /app/setup.sql"
pg_ctlcluster 16 main stop
