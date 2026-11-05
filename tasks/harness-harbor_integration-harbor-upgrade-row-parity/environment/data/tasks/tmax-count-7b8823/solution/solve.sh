#!/bin/bash
grep -c '^ERROR ' /app/service.log > /app/answer.txt
