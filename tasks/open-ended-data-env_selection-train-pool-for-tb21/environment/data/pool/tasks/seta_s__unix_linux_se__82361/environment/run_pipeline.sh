#!/bin/bash
set -euo pipefail
exec runuser -u pipeline -- python3 /srv/pipeline/process.py
