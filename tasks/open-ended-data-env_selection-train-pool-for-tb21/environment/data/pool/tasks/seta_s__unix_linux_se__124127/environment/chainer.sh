#!/bin/bash
# Spawns a subprocess then exits, leaving it running
bash -c 'while true; do sleep 5; done' &
exit 0
