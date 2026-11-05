#!/bin/bash
cd /opt/taskflow
source .venv/bin/activate
python app.py 2>&1 | tee -a logs/crash.log
