#!/bin/bash
cd /opt/batch_processor
nohup ./workers/process_batch_1.sh &
nohup ./workers/process_batch_2.sh &
nohup ./workers/process_batch_3.sh &
wait
echo "All workers finished"
