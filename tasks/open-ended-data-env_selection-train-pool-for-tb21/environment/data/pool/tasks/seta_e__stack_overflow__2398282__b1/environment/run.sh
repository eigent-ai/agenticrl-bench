#!/bin/bash
set -e
cd /app/product-updater
python3 main.py /app/data/updates.csv
