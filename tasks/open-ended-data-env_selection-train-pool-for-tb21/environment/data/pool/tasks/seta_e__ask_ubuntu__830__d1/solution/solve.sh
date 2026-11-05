#!/bin/bash
set -e

# Create the /mnt/scratch directory
mkdir -p /mnt/scratch

# Append tmpfs fstab entries
echo "tmpfs /tmp tmpfs defaults,noatime,nosuid,nodev,noexec,size=256M,mode=1777 0 0" >> /etc/fstab
echo "tmpfs /mnt/scratch tmpfs defaults,noatime,size=64M,mode=1777 0 0" >> /etc/fstab

# Mount all filesystems
mount -a

# Verify mounts are active
findmnt /tmp
findmnt /mnt/scratch

echo "All tmpfs mounts configured and active."
