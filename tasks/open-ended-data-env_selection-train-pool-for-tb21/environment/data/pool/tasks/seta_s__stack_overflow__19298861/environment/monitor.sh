#!/bin/bash
# Monitoring Pipeline
# Launches game server and pipes output through the log processor

LOGDIR="/var/log/gameserver"
LOGFILE="${LOGDIR}/events.log"
PROCESSOR="/opt/gameserver/processor.py"

mkdir -p "${LOGDIR}"

/opt/gameserver/launch.sh | python3 "${PROCESSOR}" > "${LOGFILE}"
