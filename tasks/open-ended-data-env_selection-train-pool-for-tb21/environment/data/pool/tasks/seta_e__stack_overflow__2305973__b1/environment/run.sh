#!/bin/bash
set -e
cd /app
rm -f events.db
python3 src/main.py
