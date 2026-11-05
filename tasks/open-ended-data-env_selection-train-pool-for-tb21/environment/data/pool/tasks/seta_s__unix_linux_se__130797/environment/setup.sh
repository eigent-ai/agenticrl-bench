#!/bin/bash
set -e

# Network provisioning script for multi-service setup
# Configure dummy0 interface with service addresses

modprobe dummy
ifconfig dummy0 10.99.1.1 netmask 255.255.255.0 up
ifconfig dummy0:0 10.99.1.2 netmask 255.255.255.0 up
ifconfig dummy0:1 10.99.1.3 netmask 255.255.255.0 up
ifconfig dummy0:2 10.99.1.4 netmask 255.255.255.0 up
ifconfig dummy0:3 10.99.1.5 netmask 255.255.255.255 up
ifconfig dummy0:4 10.99.1.6 netmask 255.255.255.0 up

echo "Network setup complete."
