#!/bin/bash
echo "Failing task started at $(date)"
echo "Simulating failure..."
sleep 0.5
echo "Task failed!"
exit 1
