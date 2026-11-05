#!/bin/bash
set -e
cd /app
javac DateReport.java
java -Duser.language=th -Duser.country=TH DateReport
echo "Done. Report written to /app/report.json"
