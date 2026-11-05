#!/bin/bash

mkdir -p /var/log/secureapp /var/log/nginx

cd /opt/secureapp
gunicorn -b 127.0.0.1:5000 -w 2 backend:app \
    --daemon \
    --access-logfile /var/log/secureapp/access.log \
    --error-logfile /var/log/secureapp/error.log

nginx

exec sleep infinity
