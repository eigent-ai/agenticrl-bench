#!/bin/bash
sed -i '/^path-exclude[[:space:]]*\/usr\/share\/man/d' /etc/dpkg/dpkg.cfg.d/excludes
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y --reinstall man-db coreutils passwd util-linux 2>&1 | tail -20
echo 'running mandb...'
mandb 2>&1 | tail -20
echo "mandb exit: $?"
echo 'testing man ls...'
MANPAGER=cat man ls 2>&1 | head -10
echo "man ls exit: $?"
echo 'testing man -k useradd...'
man -k useradd 2>&1
echo "man -k exit: $?"
