#!/bin/bash
cd /opt/shift-scheduler
mvn -q compile exec:java -Dexec.mainClass=scheduler.Main
