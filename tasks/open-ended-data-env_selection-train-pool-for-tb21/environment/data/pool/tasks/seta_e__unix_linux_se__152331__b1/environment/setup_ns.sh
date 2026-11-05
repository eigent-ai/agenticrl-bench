#!/bin/bash
# Namespace network setup
# Configures veth connectivity between host and ns-monitor namespace
set -e

# Move veth-ns into the monitor namespace
ip link set dev veth-ns netns ns-monitor

# Configure host-side interface
ip addr add 10.200.0.1/24 dev veth-host
ip link set dev veth-host up

# Configure namespace-side interface
ip netns exec ns-monitor ip addr add 10.200.0.2/24 dev veth-ns
ip netns exec ns-monitor ip link set dev veth-ns up
ip netns exec ns-monitor ip link set dev lo up

echo "Namespace network configured."
