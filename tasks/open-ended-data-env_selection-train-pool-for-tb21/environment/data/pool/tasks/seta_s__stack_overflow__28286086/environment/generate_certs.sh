#!/bin/bash
set -e

mkdir -p /opt/secureapp/certs
cd /opt/secureapp/certs

openssl genrsa -out ca.key 2048
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
    -out ca.crt \
    -subj "/C=US/ST=California/L=SanFrancisco/O=SecureApp CA/CN=SecureApp Root CA"

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr \
    -subj "/C=US/ST=California/L=SanFrancisco/O=SecureApp/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
    -out server.crt -days 3650 -sha256 \
    -copy_extensions copyall

rm -f server.csr ca.srl

chmod 644 ca.crt server.crt
chmod 600 ca.key server.key
