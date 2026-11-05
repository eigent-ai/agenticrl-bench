#!/bin/bash
set -a
source /etc/default/pipeline
set +a

export PYTHONPATH=/opt/pipeline/lib

python3 /opt/pipeline/run_pipeline.py
