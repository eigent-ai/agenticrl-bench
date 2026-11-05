#!/bin/bash

echo "Starting network monitoring and QoS system..."

/opt/netmon/check-ready.sh
if [ $? -ne 0 ]; then
    echo "Readiness check failed, continuing anyway..."
fi

/opt/netmon/setup-bridge.sh

/opt/netmon/monitor.sh

/opt/netmon/test-veth-setup.sh

echo "System setup complete."
