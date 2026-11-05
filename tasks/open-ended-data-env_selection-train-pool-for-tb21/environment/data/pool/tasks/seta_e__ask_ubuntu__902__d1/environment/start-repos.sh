#!/bin/bash
service apache2 start
sleep 1
apt-get update 2>/dev/null || true
