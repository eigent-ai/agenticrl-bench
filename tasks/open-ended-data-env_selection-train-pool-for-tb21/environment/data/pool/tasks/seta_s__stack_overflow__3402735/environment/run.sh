#!/bin/bash
ulimit -n 18
exec java -jar /app/target/datareporter.jar
