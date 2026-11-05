#!/bin/bash

IMG="/opt/imagebuilder/output/disk.img"
STAGING="/opt/imagebuilder/staging"

mkdir -p /opt/imagebuilder/output
rm -rf "$STAGING"
mkdir -p "$STAGING/boot/grub" "$STAGING/etc/sysconfig/network-scripts"

echo "Creating disk image..."
dd if=/dev/zero of="$IMG" bs=1M count=512

echo "Partitioning disk image..."
parted -s "$IMG" mklabel msdos
parted -s "$IMG" mkpart primary ext4 1MiB 100%

echo "Setting up GRUB modules..."
cp -r /usr/lib/grub/i386-pc "$STAGING/boot/grub/"

echo "Building GRUB core image..."
grub-mkimage -O i386-pc -o /tmp/core.img -p '/boot/grub' biosdisk part_msdos ext2

echo "Writing GRUB boot code to MBR..."
dd if=/usr/lib/grub/i386-pc/boot.img of="$IMG" bs=512 count=1 conv=notrunc
dd if=/tmp/core.img of="$IMG" bs=512 seek=1 conv=notrunc

echo "Generating device map..."
echo "(hd0) /dev/sda" > "$STAGING/boot/grub/device.map"

echo "Copying network configuration..."
cp /opt/imagebuilder/templates/ifcfg-eth0 "$STAGING/etc/sysconfig/network-scripts/ifcfg-eth0"

echo "Creating filesystem in image..."
mke2fs -F -t ext4 -d "$STAGING" -E offset=1048576 "$IMG"

echo "Build complete: $IMG"
