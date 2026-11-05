#!/bin/bash
mkdir -p /var/lib/webapp
echo '{"initialized": true, "version": 1}' > /var/lib/webapp/data.db
