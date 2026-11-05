#!/bin/bash
set -e
sudo /opt/ci/apply-config.sh
sudo echo "Deploy completed at $(date -Iseconds)" > /var/log/ci/deploy.log
echo "Deployment finished"
