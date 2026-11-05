#!/bin/bash
cd /opt/javaapps/batchjob
java -XX:+TraceClassLoading -XX:+TraceClassUnloading -XX:+AggressiveOpts -Xms128m -Xmx512m -jar lib/batchjob.jar
