#!/bin/bash
cd /opt/debugme
export LD_LIBRARY_PATH=/usr/local/lib:$(pwd)/lib
exec ./bin/app "$@"
