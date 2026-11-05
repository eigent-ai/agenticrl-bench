#!/bin/bash
# bridge-setup.sh - Configure the virtual network bridge and NAT settings
# Generates bridge and NAT configuration files under /opt/netvm/var/

NETVM_HOME=/opt/netvm
source "$NETVM_HOME/conf/network.conf"

BRIDGE_DIR="$NETVM_HOME/var/bridge"
NAT_DIR="$NETVM_HOME/var/nat"

setup_bridge() {
    mkdir -p "$BRIDGE_DIR"
    echo "br0" > "$BRIDGE_DIR/name"
    echo "$BRIDGE_IP" > "$BRIDGE_DIR/ip"
    echo "up" > "$BRIDGE_DIR/state"
}

setup_nat() {
    mkdir -p "$NAT_DIR"
    echo "MASQUERADE -s $SUBNET -o eth1" > "$NAT_DIR/postrouting"
    echo "ACCEPT -i br0" > "$NAT_DIR/forward_in"
    echo "ACCEPT -o br0" > "$NAT_DIR/forward_out"
}

setup_bridge
setup_nat
