#!/bin/bash
# Generate a unique machine fingerprint from CPU ID and MAC addresses

source /opt/hwaudit/config.sh

DMIDECODE_FILE="${DATA_DIR}/dmidecode_cpu.txt"
IFCONFIG_FILE="${DATA_DIR}/ifconfig_capture.txt"

# Extract CPU ID
cpu_id=$(grep 'ID:' "$DMIDECODE_FILE" | sed 's/.*ID://;s/ //g')

# Extract MAC addresses
mac_addrs=$(grep 'ether' "$IFCONFIG_FILE" | awk '{print $NF}' | sed 's/://')

# Combine and hash
echo "${cpu_id} ${mac_addrs}" | sha256sum | awk '{print $1}'
