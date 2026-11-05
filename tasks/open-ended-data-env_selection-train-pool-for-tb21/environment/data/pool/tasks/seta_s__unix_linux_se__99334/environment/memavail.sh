#!/bin/bash
awk '/MemFree/{printf "%d\n", $2 * 0.9 * 1024}' /proc/meminfo
