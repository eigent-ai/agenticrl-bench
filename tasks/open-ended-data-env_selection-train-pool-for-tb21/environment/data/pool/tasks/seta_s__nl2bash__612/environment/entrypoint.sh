#!/bin/bash
# Container entrypoint: start services then hand off to default shell
/opt/start_services.sh
exec "$@"
