#!/bin/bash
mkdir -p /etc/webapp
ln -sf /home/developer/webapp/frontend /var/deploy/web
ln -sf /home/developer/webapp/backend /var/deploy/api
ln -sf /home/developer/webapp/shared /var/deploy/common
ln -sf /home/developer/webapp/config/.env /etc/webapp/environment
ln -sf /home/developer/webapp/config/.secrets /etc/webapp/secrets
