#!/bin/bash
# Start Apache in the background so service restarts work correctly inside the container
apache2ctl start
exec tail -f /dev/null
