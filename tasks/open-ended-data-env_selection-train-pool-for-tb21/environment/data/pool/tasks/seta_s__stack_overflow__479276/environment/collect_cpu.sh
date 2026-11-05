#!/bin/bash
# Get the number of CPU cores
cpu_count=$(cat /proc/cpuinfo | awk '/^processor/{print $3}' | tail -1)
cpu_count=$((cpu_count + 1))
echo "$cpu_count"
