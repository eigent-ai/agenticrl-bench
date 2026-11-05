#!/bin/bash
# opsbench grader v2
cd /app
score=0
if [ "$(cd /app && python3 check.py 2>/dev/null)" = "ok" ]; then score=1; fi
printf '{"reward": "%s"}\n' "$score" > /logs/verifier/reward.json
