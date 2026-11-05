#!/bin/bash
set -e
export SHELL=/bin/sh
sudo -s << 'SCRIPT'
[[ $(id -u) -eq 0 ]] && echo "Running as root: yes" || echo "Running as root: no"
[[ -f /etc/os-release ]] && echo "OS info: available" || echo "OS info: missing"
echo "Security check complete"
SCRIPT
