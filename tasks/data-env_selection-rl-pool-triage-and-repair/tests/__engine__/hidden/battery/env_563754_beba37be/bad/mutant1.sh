#!/bin/bash
cat > /etc/modprobe.d/blacklist-rtl8xxxu.conf <<'B'
blacklist rtl8192cu
options rtl8192cu disable=1
B
update-initramfs -u || true
cat > /etc/NetworkManager/conf.d/wifi-managed.conf <<'N'
[device]
match-device=interface-name:wlan0
managed=1
N
