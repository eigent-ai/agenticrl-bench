#!/usr/bin/env bash
set -euo pipefail
Rscript /pipeline/preprocess.R
echo "Pipeline complete. Output: /pipeline/clean_data.csv"
