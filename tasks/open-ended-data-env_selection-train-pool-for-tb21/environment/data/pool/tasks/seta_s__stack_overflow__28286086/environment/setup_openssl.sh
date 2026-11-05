#!/bin/bash
set -e

if grep -q '\[system_default_sect\]' /etc/ssl/openssl.cnf; then
    sed -i '/^\[system_default_sect\]/a MaxProtocol = TLSv1.1' /etc/ssl/openssl.cnf
else
    echo "" >> /etc/ssl/openssl.cnf
    echo "[system_default_sect]" >> /etc/ssl/openssl.cnf
    echo "MaxProtocol = TLSv1.1" >> /etc/ssl/openssl.cnf
fi
