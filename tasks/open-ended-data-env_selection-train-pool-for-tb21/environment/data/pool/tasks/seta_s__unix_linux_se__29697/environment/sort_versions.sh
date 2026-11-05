#!/bin/bash
cd /opt/pipeline/data
sort deployments.log > /tmp/deployments.tmp
mv /tmp/deployments.tmp deployments.log
