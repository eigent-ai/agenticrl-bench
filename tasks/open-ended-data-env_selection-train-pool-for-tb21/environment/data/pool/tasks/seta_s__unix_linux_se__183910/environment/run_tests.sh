#!/bin/bash
set -e

export DISPLAY=:0

echo "Running find-cursor test..."
timeout 10 ./find-cursor
echo "PASS"
