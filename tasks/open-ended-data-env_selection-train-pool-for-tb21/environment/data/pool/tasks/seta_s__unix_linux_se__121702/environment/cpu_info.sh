#!/bin/bash

MODEL=$(grep "processor_name" /proc/cpuinfo | head -1 | cut -d'=' -f2)
CORES=$(grep -c "cpu_cores" /proc/cpuinfo)
VENDOR=$(grep "vendor" /proc/cpuinfo | head -1 | cut -d'=' -f2)

echo "model_name=$MODEL"
echo "cores=$CORES"
echo "vendor_id=$VENDOR"
