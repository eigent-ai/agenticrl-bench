#!/bin/bash
set -euo pipefail
exec runuser -u pipeline -- node /srv/pipeline/process.js
