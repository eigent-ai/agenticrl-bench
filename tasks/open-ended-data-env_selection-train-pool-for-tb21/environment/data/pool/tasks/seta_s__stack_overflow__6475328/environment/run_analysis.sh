#!/bin/bash
set -e
cd /opt/loganalyzer
ulimit -v 262144
python3 src/analyzer.py
