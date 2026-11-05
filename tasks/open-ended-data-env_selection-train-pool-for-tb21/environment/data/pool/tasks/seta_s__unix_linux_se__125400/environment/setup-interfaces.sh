#!/bin/bash
modprobe dummy 2>/dev/null || true
ip link add dummy0 type dummy 2>/dev/null || true
ip link add dummy1 type dummy 2>/dev/null || true
ip link add dummy2 type dummy 2>/dev/null || true
ip link set dummy0 up 2>/dev/null || true
ip link set dummy1 up 2>/dev/null || true
ip link set dummy2 up 2>/dev/null || true
ip link set dummy0 mtu 1500 2>/dev/null || true
ip link set dummy1 mtu 9000 2>/dev/null || true
ip link set dummy2 mtu 1400 2>/dev/null || true
