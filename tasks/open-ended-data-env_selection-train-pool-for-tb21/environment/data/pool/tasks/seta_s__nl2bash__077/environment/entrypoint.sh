#!/bin/bash
service cron start
exec tail -f /dev/null
