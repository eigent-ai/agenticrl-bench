#!/usr/bin/env bash
set -euo pipefail
cd /home/user/scheduler

echo "=== Compiling ==="
javac DateScheduler.java TestRunner.java

echo "=== Running TestRunner ==="
java TestRunner
