#!/bin/bash
grep -c '^ERROR ' /app/events.log > /app/answer.txt
