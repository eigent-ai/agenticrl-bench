#!/bin/bash
ssh \
    -o ServerAliveInterval=60 \
    -o ServerAliveCountMax=3 \
    -o StrictHostKeyChecking=yes \
    -i /home/tunneluser/.ssh/tunnel_key \
    -R 2225:localhost:22 \
    -p 2222 \
    tunneluser@localhost
