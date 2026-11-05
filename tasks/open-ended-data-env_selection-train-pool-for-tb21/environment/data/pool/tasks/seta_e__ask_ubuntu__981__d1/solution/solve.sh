#!/bin/bash

# Discover all configuration files (including hidden dotfiles) in the restricted directory tree
# Using sudo find which includes dotfiles by default, unlike shell globs
sudo find /home/legacy_admin/configs/ -type f -exec cp {} /home/recovery_user/recovered/ \;

# Change ownership of all recovered files (including hidden ones) to recovery_user
# Must use find since shell glob * skips dotfiles
sudo find /home/recovery_user/recovered/ -type f -exec chown recovery_user:recovery_user {} \;

# Set readable permissions on all recovered files
sudo find /home/recovery_user/recovered/ -type f -exec chmod 644 {} \;

echo "Done! All configuration files recovered."
