#!/bin/bash
# Container init: start background services then exec the main command

# Generate SSH host keys if missing
ssh-keygen -A -q

# Create required runtime directories and log file
mkdir -p /run/sshd /var/log
touch /var/log/tunnel-service.log
chown tunneluser:tunneluser /var/log/tunnel-service.log

# Start the primary sshd on port 22
/usr/sbin/sshd -f /etc/ssh/sshd_config

# Start the secondary sshd on port 2222
/usr/sbin/sshd -f /etc/ssh/sshd_config_2222

# Start the tunnel daemon as tunneluser in background.
# The & is on the outer su command so the daemon process is properly
# reparented when the su shell exits, not trapped inside a sub-shell.
su -s /bin/bash tunneluser -c \
  'exec /usr/local/bin/tunnel-daemon.sh' >> /var/log/tunnel-service.log 2>&1 &

# Brief pause so SSH daemons finish binding their ports before CMD runs
sleep 2

# Execute the provided command (agent script, verifier, or default sleep)
exec "$@"
