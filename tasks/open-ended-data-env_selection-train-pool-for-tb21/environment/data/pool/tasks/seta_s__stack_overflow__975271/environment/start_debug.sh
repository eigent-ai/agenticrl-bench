#!/bin/bash
exec java -jar /opt/app/app.jar -agentlib:jdwp=transport=dt_socket,server=y,address=8000, suspend=n
