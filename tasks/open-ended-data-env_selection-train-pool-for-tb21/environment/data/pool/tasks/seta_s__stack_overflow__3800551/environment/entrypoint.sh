#!/bin/bash
pg_ctlcluster 16 main start
sleep 2
exec bash
