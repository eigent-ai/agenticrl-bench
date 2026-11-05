#!/bin/bash

cd /opt/sortbench

./build/benchmark | awk -F',' '{print $0}' > results/report.csv
echo "Benchmark complete. Results saved to results/report.csv"
