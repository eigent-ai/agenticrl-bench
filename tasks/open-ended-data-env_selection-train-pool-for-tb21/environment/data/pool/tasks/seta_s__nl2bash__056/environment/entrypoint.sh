#!/bin/bash
# Start nginx in the background so it runs during both agent sessions and test runs
nginx

# Execute the command passed to the container (agent shell, oracle script, etc.)
exec "$@"
