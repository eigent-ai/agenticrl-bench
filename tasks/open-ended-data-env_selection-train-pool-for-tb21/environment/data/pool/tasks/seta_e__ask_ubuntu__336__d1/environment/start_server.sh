#!/bin/bash
python3 -m http.server 8765 --directory /app/media > /dev/null 2>&1 &
echo "Server started on port 8765"
