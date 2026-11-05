#!/bin/bash
set -e

DISK=/opt/disk.img
MOUNT_EFI=/mnt/efi

LOOP=$(losetup --find --show "$DISK")

mkdir -p $MOUNT_EFI

mount ${LOOP} $MOUNT_EFI

grub-install \
    --target=x86_64-efi \
    --efi-directory=/mnt/boot \
    --bootloader-id=GRUB \
    --recheck

echo "GRUB installed successfully"

umount $MOUNT_EFI
losetup -d $LOOP
