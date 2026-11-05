#!/bin/bash
echo "=== Current EFI Boot Configuration ==="
efibootmgr -v
echo ""
echo "=== Checking EFI files on disk ==="
for dir in /boot/efi/EFI/*/; do
    echo "Directory: $dir"
    ls -la "$dir" 2>/dev/null
done
echo ""
echo "=== Removing duplicate entries ==="
efibootmgr -b 0005 -B
efibootmgr -b 0007 -B
echo ""
echo "=== Removing orphan/invalid entries ==="
efibootmgr -b 0006 -B
efibootmgr -b 0008 -B
echo ""
echo "=== Setting correct boot order ==="
efibootmgr -o 0001,0003,0002,0004
echo ""
echo "=== Setting boot timeout ==="
efibootmgr -t 3
echo ""
echo "=== Final EFI Boot Configuration ==="
efibootmgr -v
