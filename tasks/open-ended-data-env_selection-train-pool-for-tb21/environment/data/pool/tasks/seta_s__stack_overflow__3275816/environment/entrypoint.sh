#!/bin/bash

# Start nginx
nginx

# Start dashboard application
/opt/dashboard/run.sh &

# Start widgets application
/opt/widgets/run.sh &

# Keep container alive
exec sleep infinity
