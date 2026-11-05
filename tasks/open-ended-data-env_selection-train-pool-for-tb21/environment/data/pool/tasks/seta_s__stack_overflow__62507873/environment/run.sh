#!/bin/bash
set -e
mkdir -p /opt/resample_pipeline/output
cd /opt/resample_pipeline
Rscript resample.R
echo "Pipeline complete. Output: /opt/resample_pipeline/output/resampled.csv"
