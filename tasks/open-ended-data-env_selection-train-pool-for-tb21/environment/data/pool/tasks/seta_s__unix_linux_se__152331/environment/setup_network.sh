#!/bin/bash
# Lab network setup
# Configures bridge br-lab (172.16.100.1/24) with virtual member eth-lab

set -e

# Create and bring up the bridge
ip link add name br-lab type bridge
ip link set dev br-lab up

# Assign address to bridge
ip addr add 172.16.100.1/24 brd + dev br-lab

# Attach member interface to bridge
ip link set dev eth-lab master br-lab

echo "Lab network configured."
