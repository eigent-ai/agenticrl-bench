#!/bin/bash
echo "CPU Usage: $(grep cpu /proc/stat | head -1)"
