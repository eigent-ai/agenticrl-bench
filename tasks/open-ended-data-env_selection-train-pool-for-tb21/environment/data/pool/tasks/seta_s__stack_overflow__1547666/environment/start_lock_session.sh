#!/bin/bash
pg_ctlcluster 16 main start 2>/dev/null || true
sleep 2
sudo -u postgres psql -d proddb -c "BEGIN; LOCK TABLE customer_accounts IN ACCESS EXCLUSIVE MODE;" &
sleep 2
