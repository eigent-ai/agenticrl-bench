#!/bin/bash
set -e
cd /app
mkdir -p classes
rm -f classes/*.class
javac -cp lib/h2.jar src/*.java -d classes
java -Duser.timezone=UTC \
     -cp classes:lib/h2.jar \
     Main
