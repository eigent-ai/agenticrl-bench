#!/bin/bash
# Outputs a qemu-system-x86_64 invocation for the development VM.
# Usage: generate-cmd.sh [disk-image [memory-mb]]
set -euo pipefail

ACCEL=$(kvm-detect.sh)
DISK="${1:-/var/lib/vm/disk.qcow2}"
MEM="${2:-512}"
BRIDGE="${BRIDGE:-devbridge}"

case "$ACCEL" in
    kvm)
        printf 'qemu-system-x86_64 -machine type=pc -cpu host -enable-kvm -m %s -drive file=%s,format=qcow2,if=virtio -net nic,model=virtio -net bridge,br=%s -nographic\n' \
            "$MEM" "$DISK" "$BRIDGE"
        ;;
    tcg)
        printf 'qemu-system-x86_64 -machine type=pc,accel=tcg -m %s -drive file=%s,format=raw,if=ide -net nic,model=e1000 -net bridge,br=%s -nographic\n' \
            "$MEM" "$DISK" "$BRIDGE"
        ;;
esac
