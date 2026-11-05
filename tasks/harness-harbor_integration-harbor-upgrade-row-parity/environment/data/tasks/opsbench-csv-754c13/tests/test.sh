#!/bin/bash
# opsbench grader v2
cd /app
score=0
if [ "$(tr -d "[:space:]" < /app/total.txt 2>/dev/null)" = "558" ]; then score=1; fi
printf '{"score": "%s"}\n' "$score" > /logs/verifier/reward.json
