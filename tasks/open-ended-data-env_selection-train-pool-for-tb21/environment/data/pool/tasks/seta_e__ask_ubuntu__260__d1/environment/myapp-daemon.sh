#!/bin/bash
while true; do
  echo "App daemon running at $(date)" >> /var/log/myapp.log
  sleep 10
done
