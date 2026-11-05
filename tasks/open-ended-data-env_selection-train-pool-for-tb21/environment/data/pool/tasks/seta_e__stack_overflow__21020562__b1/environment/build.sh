#!/bin/bash
set -e
cd /app
go build -o pipeline .
echo "Build successful."
