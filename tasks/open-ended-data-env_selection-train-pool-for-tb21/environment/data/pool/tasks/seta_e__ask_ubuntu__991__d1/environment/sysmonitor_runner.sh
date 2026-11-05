#!/bin/bash
# Runner script for sysmonitor
# This script activates the virtual environment and runs the sysmonitor application

/opt/sysmonitor/venv/bin/python3 /opt/sysmonitor/sysmonitor.py "$@"
