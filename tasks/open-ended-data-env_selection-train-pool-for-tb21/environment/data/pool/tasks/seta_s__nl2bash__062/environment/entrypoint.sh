#!/bin/bash
nice -n 15 sleep 3600 &
echo $! > /tmp/lo_pri_pid

nice -n 5 sleep 3600 &
echo $! > /tmp/mid_pri_pid

sleep 3600 &
echo $! > /tmp/normal_pid

exec tail -f /dev/null
