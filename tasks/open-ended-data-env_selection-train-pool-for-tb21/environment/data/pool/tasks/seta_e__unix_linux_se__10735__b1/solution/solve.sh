#!/bin/bash
set -e

# Fix authbind configuration: create byport authorization file for port 80
touch /etc/authbind/byport/80
chown webuser:webuser /etc/authbind/byport/80
chmod 500 /etc/authbind/byport/80

# Fix config file permissions: make it readable by webuser
chmod 644 /etc/webapp/config.yaml
