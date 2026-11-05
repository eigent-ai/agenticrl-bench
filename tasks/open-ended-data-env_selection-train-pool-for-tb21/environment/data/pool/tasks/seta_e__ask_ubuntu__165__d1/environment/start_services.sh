#!/bin/bash
service rsyslog start
service cron start
tail -f /dev/null
