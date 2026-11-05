#!/bin/bash
# opsbench grader v2
cd /app
score=0
if [ "$(tr -d "[:space:]" < /app/answer.txt 2>/dev/null)" = "3" ]; then score=1; fi
printf '{"reward": "%s"}\n' "$score" > /logs/verifier/reward.json
