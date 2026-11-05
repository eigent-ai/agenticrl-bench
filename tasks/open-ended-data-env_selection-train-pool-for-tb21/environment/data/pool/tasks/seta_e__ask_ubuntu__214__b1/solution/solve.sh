#!/bin/bash

# Copy the internal CA certificate to the system CA certificates directory
cp /app/certs/internal-ca.crt /usr/local/share/ca-certificates/internal-ca.crt

# Update the system trust store to incorporate the new CA
update-ca-certificates

# Run the health-check script to verify all services are healthy
/app/health_check.sh

echo "Done!"
