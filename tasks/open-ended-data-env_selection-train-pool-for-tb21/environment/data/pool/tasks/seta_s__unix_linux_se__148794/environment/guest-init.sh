#!/bin/bash
set -e

HOSTNAME="{{HOSTNAME}}"

apt-get update
apt-get install -y vim curl wget

hostnamectl set-hostname "$HOSTNAME"
echo "$HOSTNAME" > /etc/hostname
sed -i "s/127.0.1.1.*/127.0.1.1\t${HOSTNAME}/" /etc/hosts

systemctl enable ssh
systemctl start ssh

echo "Guest initialization complete for $HOSTNAME"
