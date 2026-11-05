#!/bin/bash
rm -rf /var/deploy/web
rm -rf /var/deploy/api
rm -rf /var/deploy/common
ln -s /home/developer/webapp/frontend /var/deploy/web
ln -s /home/developer/webapp/backend /var/deploy/api
ln -s /home/developer/webapp/shared /var/deploy/common
mkdir -p /etc/webapp
ln -s /home/developer/webapp/config/.env /etc/webapp/environment
ln -s /home/developer/webapp/config/.secrets /etc/webapp/secrets
