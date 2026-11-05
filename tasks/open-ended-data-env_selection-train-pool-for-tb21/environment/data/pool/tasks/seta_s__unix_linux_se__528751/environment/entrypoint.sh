#!/bin/bash
# Start nginx so the local package server is available
nginx 2>/dev/null || true
exec "$@"
