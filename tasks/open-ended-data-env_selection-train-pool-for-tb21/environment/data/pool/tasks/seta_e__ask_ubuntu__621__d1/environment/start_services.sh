#!/bin/bash
# Initialize PostgreSQL if needed
if [ ! -d "/var/lib/postgresql/16/main" ]; then
    sudo -u postgres /usr/lib/postgresql/16/bin/initdb -D /var/lib/postgresql/16/main
fi

# Start supervisor (manages nginx, flask, postgresql)
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf
sleep 3

# Verify services are running
supervisorctl status
