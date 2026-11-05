#!/bin/bash
set -e
bash /opt/pipeline/sort_inventory.sh
bash /opt/pipeline/sort_latency.sh
bash /opt/pipeline/sort_versions.sh
echo "Pipeline complete."
