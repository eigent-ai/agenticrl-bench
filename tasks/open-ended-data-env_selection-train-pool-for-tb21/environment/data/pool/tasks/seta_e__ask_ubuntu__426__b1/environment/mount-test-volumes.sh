#!/bin/sh
mount -o loop /tmp/data1.img /mnt/data1 2>/dev/null || true
mount -o loop /tmp/data2.img /mnt/data2 2>/dev/null || true
