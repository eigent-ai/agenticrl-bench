#!/bin/bash
# Pre-provision hook
# Sets environment variables used during provisioning

PROVISION_TIMESTAMP=$(date +"%Y-%m-%dT%H:%M:%S)
PROVISIONER="workspace-manager-v2"

export PROVISION_TIMESTAMP
export PROVISIONER
