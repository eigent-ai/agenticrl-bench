#!/bin/bash
set -e
cd /opt/quarterutil
go build -o quarterutil .
echo "Build successful."
