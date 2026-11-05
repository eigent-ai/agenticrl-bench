#!/bin/bash
set -e
service mysql start
sleep 3
exec tail -f /dev/null
