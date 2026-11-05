#!/bin/bash
# Start the pipeline worker in background
nohup /usr/bin/python3 /opt/pipeline/pipeline_worker.py > /dev/null 2>&1 &
