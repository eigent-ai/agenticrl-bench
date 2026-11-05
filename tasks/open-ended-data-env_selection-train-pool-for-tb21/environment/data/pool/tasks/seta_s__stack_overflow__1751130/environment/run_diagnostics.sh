#!/bin/bash
JMX_PORT=9020
JMX_HOST=localhost
JMXTERM=/opt/tools/jmxterm.jar

OUTPUT=$(echo "bean com.warehouse:type=Diagnostics
run runDiagnostics" | java -jar $JMXTERM -l ${JMX_HOST}:${JMX_PORT} -u admin -p adminPass -n -v silent 2>&1)
RC=$?

if [ $RC -eq 0 ] && ! echo "$OUTPUT" | grep -qi "exception\|denied\|refuse"; then
    echo "$OUTPUT"
    exit 0
else
    echo "Diagnostics failed"
    echo "$OUTPUT"
    exit 1
fi
