#!/bin/bash
source /opt/tunnels/tunnel.conf

ssh -f -N -L ${registry_local_port}:localhost:${registry_remote_port} ${bastion_host}
ssh -f -N -L ${api_local_port}:localhost:${api_remote_port} ${bastion_host}
