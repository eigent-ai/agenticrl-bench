#!/bin/bash
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
cpu_idle=$(top -bn1 | grep 'Cpu(s)' | awk '{print $8}')
mem_used=$(free -m | awk '/Mem:/{print $3}')
mem_total=$(free -m | awk '/Mem:/{print $2}')
echo "${timestamp} - CPU Idle: ${cpu_idle}% | Memory: ${mem_used}/${mem_total}MB"
