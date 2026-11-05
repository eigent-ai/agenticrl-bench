#!/bin/bash
set -e

echo "=== Installing build dependencies ==="
apt-get build-dep -y libxml2

echo "=== Building project ==="
cd "$(dirname "$0")"
make clean
make

echo "=== Installing ==="
make install

echo "=== Running ==="
/opt/buildproject/buildproject
