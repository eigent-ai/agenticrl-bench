#!/bin/bash
runuser -u webuser -- web_worker infinity &
sleep 0.3
runuser -u dbuser -- db_worker infinity &
sleep 0.3
log_collector infinity &
sleep 0.3
exec "${@:-sleep infinity}"
