#!/bin/bash
echo '=== Packages marked as auto-installed ==='
apt-mark showauto
echo ''
echo '=== Packages that would be autoremoved ==='
apt-get autoremove --dry-run
echo ''
echo '=== Packages on hold ==='
apt-mark showhold
