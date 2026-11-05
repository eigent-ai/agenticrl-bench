#!/bin/bash
echo "=== Current EFI Boot Configuration ==="
efibootmgr -v
echo ""
echo "=== Removing duplicate entries ==="
efibootmgr -b 0005 -B
efibootmgr -b 0007 -B
echo ""
echo "=== Removing invalid entries ==="
efibootmgr -b 0006 -B
efibootmgr -b 0008 -B
echo ""
echo "=== Setting correct boot order ==="
efibootmgr -o 0001,0003,0002,0004
echo ""
echo "=== Final EFI Boot Configuration ==="
efibootmgr -v
