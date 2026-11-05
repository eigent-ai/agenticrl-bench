#!/bin/bash
echo "Starting appserver..."
/usr/bin/python3 -m http.server 8111 --directory /opt/appserver/data
