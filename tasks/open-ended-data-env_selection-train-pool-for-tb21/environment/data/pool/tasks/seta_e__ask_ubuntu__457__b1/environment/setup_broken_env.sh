#!/bin/bash
export HTTP_PROXY="http://127.0.0.1:8888"
export HTTPS_PROXY="http://127.0.0.1:8888"
export http_proxy="http://127.0.0.1:8888"
export https_proxy="http://127.0.0.1:8888"

# Start tinyproxy with restrictive config
tinyproxy -c /etc/tinyproxy/tinyproxy.conf &
sleep 1

echo "Proxy environment configured."
