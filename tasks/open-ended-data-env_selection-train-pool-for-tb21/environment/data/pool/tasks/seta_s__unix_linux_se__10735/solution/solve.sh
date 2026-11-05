#!/bin/bash
set -e

# Grant the binary the capability to bind to privileged ports as a non-root user
setcap 'cap_net_bind_service=+ep' /usr/local/bin/apiserver

# Make the config file readable by apiuser
chmod 644 /etc/apiserver/config.json
