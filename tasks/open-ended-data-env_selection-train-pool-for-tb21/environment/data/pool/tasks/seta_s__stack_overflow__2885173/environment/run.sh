#!/bin/bash
cd /opt/csvreporter
mkdir -p output build
javac -d build src/SummaryWriter.java src/DepartmentAggregator.java src/FilteredReportWriter.java src/Main.java
java -cp build Main
