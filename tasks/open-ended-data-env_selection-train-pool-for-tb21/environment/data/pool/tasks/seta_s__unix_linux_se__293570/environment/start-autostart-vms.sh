#!/bin/bash
# Restart all autostart-enabled virtual machines
# Run this script after a maintenance window to bring VMs back online

for vm in $(virsh list --autostart); do
    virsh start "$vm" || true
done
