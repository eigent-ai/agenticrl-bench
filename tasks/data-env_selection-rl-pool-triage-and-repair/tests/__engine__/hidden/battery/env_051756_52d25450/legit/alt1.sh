#!/bin/bash
set -eu
conf_dir=/etc/openvpn/client
conf=$conf_dir/connection.ovpn
unit=/etc/systemd/system/openvpn-client.service
certs=/etc/openvpn/certs
install -d -m 0755 "$conf_dir" /etc/systemd/system
ovpn_bin=$(command -v openvpn || echo /usr/sbin/openvpn)
{
  printf '%s\n' \
    'client' \
    'dev tun' \
    'remote 10.0.0.2 1194 udp' \
    'nobind' \
    'resolv-retry infinite' \
    'remote-cert-tls server' \
    "ca $certs/ca.crt" \
    "cert $certs/client.crt" \
    "key $certs/client.key" \
    'persist-key' \
    'persist-tun' \
    'verb 3'
} > "$conf"
chmod 0600 "$conf"
{
  echo '[Unit]'
  echo 'Description=OpenVPN client service (connection to 10.0.0.2)'
  echo 'After=network-online.target'
  echo 'Wants=network-online.target'
  echo
  echo '[Service]'
  echo 'Type=simple'
  echo "ExecStart=$ovpn_bin --config $conf"
  echo 'Restart=on-failure'
  echo 'RestartSec=5'
  echo
  echo '[Install]'
  echo 'WantedBy=multi-user.target'
} > "$unit"
chmod 0644 "$unit"
