#!/bin/bash
WAREHOUSE_HOME=/opt/warehouse
JAVA_OPTS="-Dcom.sun.management.jmxremote \
  -Dcom.sun.management.jmxremote.port=9010 \
  -Dcom.sun.management.jmxremote.rmi.port=9010 \
  -Dcom.sun.management.jmxremote.ssl=true \
  -Dcom.sun.management.jmxremote.authenticate=true \
  -Dcom.sun.management.jmxremote.password.file=${WAREHOUSE_HOME}/conf/jmx.password \
  -Dcom.sun.management.jmxremote.access.file=${WAREHOUSE_HOME}/conf/jmx.access \
  -Dcom.sun.management.jmxremote.local.only=false \
  -Djava.rmi.server.hostname=localhost"

cd ${WAREHOUSE_HOME}
nohup java ${JAVA_OPTS} -cp ${WAREHOUSE_HOME}/lib/warehouse-service.jar com.warehouse.WarehouseService >> ${WAREHOUSE_HOME}/logs/service.log 2>&1 &
echo $! > ${WAREHOUSE_HOME}/logs/service.pid
echo "Service started with PID $(cat ${WAREHOUSE_HOME}/logs/service.pid)"
