#!/bin/bash
set -e
mkdir -p /project/out
javac -encoding UTF-8 -d /project/out /project/src/DateUtils.java /project/src/DateUtilsDriver.java
echo "Compilation successful."
