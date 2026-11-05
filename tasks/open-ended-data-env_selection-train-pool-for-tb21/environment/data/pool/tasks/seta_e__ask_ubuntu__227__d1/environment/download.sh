#!/bin/bash
# download.sh - Data pipeline download script
# Downloads protected data from the HTTP endpoint

wget http://$AUTH_USERNAME:$AUTH_PASSWORD@localhost:8080/data.txt -O /tmp/data.txt

echo "Download complete. File saved."
