#!/bin/bash
grep -c '^WARN ' /app/events.log > /app/answer.txt
