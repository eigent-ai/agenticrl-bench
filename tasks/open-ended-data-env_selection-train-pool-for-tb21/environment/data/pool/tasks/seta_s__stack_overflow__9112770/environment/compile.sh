#!/usr/bin/env bash
set -e
mkdir -p /app/out
javac -cp /app/lib/h2.jar -d /app/out /app/src/DateUtils.java
