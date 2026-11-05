#!/bin/bash
cd /app
if [ "$(tr -d "[:space:]" < /app/answer.txt 2>/dev/null)" = "6" ]; then echo 1 > /logs/verifier/reward.txt; else echo 0 > /logs/verifier/reward.txt; fi
