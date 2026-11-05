#!/bin/bash
rm -f /run/ssh-agent.sock

# eval $(ssh-agent -a ...) is synchronous: socket is guaranteed ready before eval returns
eval $(ssh-agent -a /run/ssh-agent.sock) > /dev/null

# OpenSSH 9.x ownership check: ssh-add refuses keys not owned by the calling user.
# Temporarily chown key files to root, load them, then restore original ownership.
chown root:root /home/alice/.ssh/id_rsa /home/charlie/.ssh/id_ed25519

SSH_AUTH_SOCK=/run/ssh-agent.sock ssh-add \
    /home/alice/.ssh/id_rsa \
    /home/charlie/.ssh/id_ed25519 > /dev/null 2>&1

chown alice:alice /home/alice/.ssh/id_rsa
chown charlie:charlie /home/charlie/.ssh/id_ed25519

exec "$@"
