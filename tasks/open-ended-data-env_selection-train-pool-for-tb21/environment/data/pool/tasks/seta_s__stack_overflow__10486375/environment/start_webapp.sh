#!/bin/bash
cd /opt/javaapps/webapp
java -XX:+PrintGC -XX:+PrintGCDetails -XX:MaxPermSize=256m -XX:+UseConcMarkSweepGC -Xms256m -Xmx1024m -jar lib/webapp.jar
