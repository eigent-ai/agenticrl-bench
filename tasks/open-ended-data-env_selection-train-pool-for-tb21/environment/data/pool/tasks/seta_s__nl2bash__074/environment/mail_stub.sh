#!/bin/bash
SUBJECT="(no subject)"
while getopts "s:" opt; do
  case $opt in s) SUBJECT="$OPTARG" ;; esac
done
BODY=$(cat)
echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT subject='${SUBJECT}' body='${BODY}'" \
  >> /var/log/pg_monitor/alerts.log
