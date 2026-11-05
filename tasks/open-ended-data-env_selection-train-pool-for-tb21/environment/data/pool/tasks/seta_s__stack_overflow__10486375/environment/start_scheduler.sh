#!/bin/bash
cd /opt/javaapps/scheduler
java -XX:+UseConcMarkSweepGC -XX:+PrintCompressedOopsMode -XX:+UnsyncloadClass -Xms64m -Xmx256m -jar lib/scheduler.jar
