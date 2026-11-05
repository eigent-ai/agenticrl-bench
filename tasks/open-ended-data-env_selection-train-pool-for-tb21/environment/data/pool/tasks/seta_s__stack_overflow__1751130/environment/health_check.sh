#!/bin/bash
JMX_PORT=9020
JMX_HOST=localhost
JMXTERM=/opt/tools/jmxterm.jar

UPTIME=$(echo "bean com.warehouse:type=WarehouseStats
get UptimeSeconds" | java -jar $JMXTERM -l ${JMX_HOST}:${JMX_PORT} -u monitor -p controlPass -n -v silent 2>&1)
RC=$?

if [ $RC -eq 0 ] && echo "$UPTIME" | grep -qE '[0-9]+'; then
    echo "STATUS: OK"
    echo "Uptime: ${UPTIME}s"
    exit 0
else
    echo "STATUS: FAIL"
    echo "Details: $UPTIME"
    exit 1
fi
