#!/bin/bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/server.key \
    -out /etc/nginx/ssl/server.crt \
    -subj "/C=US/ST=State/L=City/O=Company/CN=localhost" 2>/dev/null
systemctl enable webapp nginx
systemctl start webapp nginx
exec sleep infinity
