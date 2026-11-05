#!/bin/bash
# Start the data ingestion pipeline
cd /opt/pipeline
./ingest_daemon stage1 4 &
./ingest_daemon stage2 3 &
sleep 2
echo "Pipeline started."
