#!/bin/bash
cd /app
mkdir -p bin
javac -d bin src/TimeUtils.java src/ScheduleConverter.java
java -Duser.timezone=UTC -cp bin ScheduleConverter
