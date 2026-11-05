#!/bin/bash
modprobe ecryptfs 2>&1 || echo "modprobe failed"
echo "ecryptfs loaded: $(lsmod | grep -c ecryptfs 2>/dev/null || echo 0)"

META=/mnt/recovery/.ecryptfs/analyst/.ecryptfs
PRIV=/mnt/recovery/.ecryptfs/analyst/.Private
mkdir -p "$META" "$PRIV" /mnt/plain

LOGIN_PASS="An@lyst2024"
MOUNT_PASS=$(openssl rand -hex 32)
echo "MOUNT_PASS length: ${#MOUNT_PASS}  value: $MOUNT_PASS"

# Wrap (same as entrypoint)
printf "%s" "$MOUNT_PASS" | ecryptfs-wrap-passphrase "$META/wrapped-passphrase" "$LOGIN_PASS" 2>&1
echo "Wrap exit: $?"
ls -la "$META/"

echo "=== Test 1: pipe with newline + dash ==="
R1=$(printf "%s\n" "$LOGIN_PASS" | ecryptfs-unwrap-passphrase "$META/wrapped-passphrase" - 2>&1)
E1=$?
echo "Exit=$E1 Result=[$R1]"

echo "=== Test 2: passphrase as 2nd arg ==="
R2=$(ecryptfs-unwrap-passphrase "$META/wrapped-passphrase" "$LOGIN_PASS" 2>&1)
E2=$?
echo "Exit=$E2 Result=[$R2]"

echo "=== Test 3: pipe no newline + dash ==="
R3=$(printf "%s" "$LOGIN_PASS" | ecryptfs-unwrap-passphrase "$META/wrapped-passphrase" - 2>&1)
E3=$?
echo "Exit=$E3 Result=[$R3]"

echo "=== ecryptfs-unwrap-passphrase binary location and version ==="
which ecryptfs-unwrap-passphrase
strings $(which ecryptfs-unwrap-passphrase) | grep -i "usage\|passphrase\|stdin" | head -10 || true
