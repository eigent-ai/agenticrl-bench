#!/bin/bash
# Wrapper script that starts the Node.js application.
# There may be issues with how this script launches the process.

echo "Starting webapp via wrapper..."

# Running as background process
node /app/server.js &

# Wait for the child process
wait
