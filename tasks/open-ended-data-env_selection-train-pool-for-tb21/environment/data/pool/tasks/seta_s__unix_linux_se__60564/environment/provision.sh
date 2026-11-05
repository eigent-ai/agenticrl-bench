#!/bin/bash
DOMAIN="webserver"
XML_PATH="/opt/vmtools/vms/webserver.xml"

echo "Registering domain: $DOMAIN"
virsh create "$XML_PATH"
if [ $? -eq 0 ]; then
    echo "Domain $DOMAIN registered successfully."
else
    echo "ERROR: Failed to register domain $DOMAIN" >&2
    exit 1
fi
