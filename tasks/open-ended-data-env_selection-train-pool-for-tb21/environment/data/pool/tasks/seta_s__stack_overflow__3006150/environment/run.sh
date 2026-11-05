#!/bin/bash
cd /app
mvn -q package -DskipTests && java -cp target/classes com.reports.EventProcessor 2025-01-01 src/main/resources/events.csv output/report.json
