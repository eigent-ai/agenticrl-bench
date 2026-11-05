#!/bin/sh
mkdir -p /etc/runlevels/development
mkdir -p /etc/runlevels/staging
mkdir -p /etc/runlevels/production

ln -s /etc/init.d/app-dev /etc/runlevels/development/app-dev
ln -s /etc/init.d/app-staging /etc/runlevels/staging/app-staging
ln -s /etc/init.d/database /etc/runlevels/staging/database
ln -s /etc/init.d/app-prod /etc/runlevels/production/app-prod
ln -s /etc/init.d/database /etc/runlevels/production/database
