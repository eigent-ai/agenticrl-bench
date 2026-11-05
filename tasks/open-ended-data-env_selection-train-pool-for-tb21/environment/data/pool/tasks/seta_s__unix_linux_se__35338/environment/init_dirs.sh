#!/bin/bash
set -e
su -c mkdir /var/app/uploads appuser
su -c mkdir /var/app/sessions appuser
su -c mkdir /var/app/cache appuser
echo "Application directories initialized"
