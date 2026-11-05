#!/bin/bash
pkill -TERM -x whoopsie 2>/dev/null || true
sleep 1
pkill -KILL -x whoopsie 2>/dev/null || true
rm -f /etc/systemd/system/multi-user.target.wants/whoopsie.service /etc/systemd/system/multi-user.target.wants/whoopsie.path
ln -sfn /dev/null /etc/systemd/system/whoopsie.service
