#!/bin/bash
python3 /opt/apps/jboss-web-01.py &
python3 /opt/apps/jboss-web-02.py &
python3 /opt/apps/jboss-worker-01.py &
python3 /opt/apps/jboss-worker-02.py &
python3 /opt/apps/jboss-admin-console.py &
sleep 2
exec sleep infinity
