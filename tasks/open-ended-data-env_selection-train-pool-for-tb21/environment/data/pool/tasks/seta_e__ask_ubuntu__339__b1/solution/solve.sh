#!/bin/bash

# Update package metadata
dnf makecache

# Reinstall the Development Tools group
dnf group install development-tools -y

# Install specific packages that may not be part of the group or were separately removed
dnf install -y autoconf automake gdb gcc make

# Verify the group is installed
dnf group list --installed

# Verify key packages
rpm -q gcc make autoconf automake gdb

# Check package database consistency
dnf check

echo "Recovery complete."
