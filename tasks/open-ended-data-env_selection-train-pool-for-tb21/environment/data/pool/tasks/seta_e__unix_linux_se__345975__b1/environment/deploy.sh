#!/bin/bash
# Deployment script for nginx reverse proxy
# Tests configuration and reloads nginx

echo "Testing nginx configuration..."
/usr/local/sbin/nginx -t
if [ $? -eq 0 ]; then
    echo "Config OK, reloading nginx..."
    /usr/local/sbin/nginx -s reload
    echo "Nginx reloaded successfully."
else
    echo "Config test failed! Please fix the configuration."
    exit 1
fi
