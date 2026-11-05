#!/bin/bash
# Main pipeline runner
cd /app/pipeline
./extract.sh
./filter.sh
./summarize.sh
