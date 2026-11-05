#!/bin/bash
grep -c '^WARN ' /app/service.log > /app/answer.txt
