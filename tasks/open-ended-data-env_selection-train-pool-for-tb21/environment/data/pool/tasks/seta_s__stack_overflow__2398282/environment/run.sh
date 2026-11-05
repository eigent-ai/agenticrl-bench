#!/bin/bash
set -e
cd /app/product-updater
mvn -q compile -DskipTests
java -Xmx256m -cp "target/classes:target/lib/*" com.batch.Main /app/data/updates.csv
