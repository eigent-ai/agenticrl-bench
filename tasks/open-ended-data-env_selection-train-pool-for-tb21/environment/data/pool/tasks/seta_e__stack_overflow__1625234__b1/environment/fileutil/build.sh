#!/bin/bash
set -e
cd /opt/fileutil
mkdir -p bin
go build -o bin/fileutil .
echo "Build successful."
