#!/bin/bash
cd /opt/javaapps/apiserver
java -XX:+PrintGC -XX:+UseMembar -XX:+PrintSafepointStatistics -XX:PrintSafepointStatisticsCount=1 -Xms512m -Xmx2048m -XX:+UseG1GC -jar lib/apiserver.jar
