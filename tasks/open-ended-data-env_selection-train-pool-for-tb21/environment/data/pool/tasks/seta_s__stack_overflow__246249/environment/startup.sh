#!/bin/bash
cd /opt/calmgr/feeds
python3 -m http.server 8000 &
exec "$@"
