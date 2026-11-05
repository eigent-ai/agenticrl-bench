#!/bin/sh

PREREQS="dropbear-initramfs"

prereqs()
{
    echo "$PREREQS"
}

case $1 in
prereqs)
    prereqs
    exit 0
    ;;
esac

. /usr/share/initramfs-tools/hook-functions

if [ -x /usr/lib/cryptsetup/askpass ]; then
    copy_exec /usr/lib/cryptsetup/askpass /usr/lib/cryptsetup/askpass
fi

exit 0
