#!/bin/bash

python3 -m pytest /tests/test_outputs.py -v --tb=short -rA 2>&1

if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
