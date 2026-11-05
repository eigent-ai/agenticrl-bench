#!/bin/bash
cd /opt/pipeline/data
awk '{print $NF,$0}' server_latency.txt | sort -rn | cut -d' ' -f2- > server_latency.txt
