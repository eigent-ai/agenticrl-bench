#!/bin/bash

PARAMS=$(cat /proc/sys/kernel)
echo "hostname=$(echo "$PARAMS" | grep hostname)"
echo "osrelease=$(echo "$PARAMS" | grep osrelease)"
echo "ostype=$(echo "$PARAMS" | grep ostype)"
