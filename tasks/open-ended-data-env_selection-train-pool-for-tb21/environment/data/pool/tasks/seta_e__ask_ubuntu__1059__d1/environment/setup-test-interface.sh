#!/bin/bash
# Setup dummy network interface for testing
ip link add eth1 type dummy 2>/dev/null || true
ip addr add 192.168.100.10/24 dev eth1 2>/dev/null || true
ip link set eth1 up 2>/dev/null || true
