#!/bin/bash
nice -n 15 sleep 99999 &
nice -n 18 sleep 99999 &
nice -n 12 sleep 99999 &
nice -n 5  sleep 99999 &
nice -n 0  bash -c 'while true; do sleep 1; done' &
exec sleep infinity
