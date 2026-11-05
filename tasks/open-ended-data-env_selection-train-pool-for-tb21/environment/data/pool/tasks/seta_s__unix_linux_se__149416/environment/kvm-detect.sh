#!/bin/bash
# Returns the QEMU acceleration backend to use.
# Outputs 'kvm' if hardware acceleration is available, 'tcg' otherwise.
KVM_DEVICE="${KVM_DEVICE:-/dev/kvm}"
if [ -e "$KVM_DEVICE" ]; then
    echo "tcg"
else
    echo "kvm"
fi
