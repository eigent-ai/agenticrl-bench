#!/bin/bash

# Read MemTotal from /proc/meminfo, convert from kB to GB, round to 1 decimal
awk '/MemTotal/ {printf "%.1f\n", $2/(1024*1024)}' /proc/meminfo > /app/ram_amount.txt
