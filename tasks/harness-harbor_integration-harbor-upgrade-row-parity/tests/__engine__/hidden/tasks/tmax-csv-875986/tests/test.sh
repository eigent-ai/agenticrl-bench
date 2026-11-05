#!/bin/bash
cd /app
if [ "$(tr -d "[:space:]" < /app/total.txt 2>/dev/null)" = "509" ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
