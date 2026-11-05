#!/bin/bash
set -eu
GRUB_DEFAULTS=/etc/default/grub
if grep -q '^GRUB_CMDLINE_LINUX_DEFAULT=' "$GRUB_DEFAULTS"; then
    current=$(sed -n 's/^GRUB_CMDLINE_LINUX_DEFAULT="\(.*\)"[[:space:]]*$/\1/p' "$GRUB_DEFAULTS" | tail -n1)
    case " $current " in
        *" text "*) new=$current ;;
        *) new=${current:+$current }text ;;
    esac
    sed -i "s|^GRUB_CMDLINE_LINUX_DEFAULT=.*|GRUB_CMDLINE_LINUX_DEFAULT=\"$new\"|" "$GRUB_DEFAULTS"
else
    echo 'GRUB_CMDLINE_LINUX_DEFAULT="text"' >> "$GRUB_DEFAULTS"
fi
grep '^GRUB_CMDLINE_LINUX_DEFAULT=' "$GRUB_DEFAULTS"
unit=/usr/lib/systemd/system/multi-user.target
[ -e "$unit" ] || unit=/lib/systemd/system/multi-user.target
mkdir -p /etc/systemd/system
ln -sf "$unit" /etc/systemd/system/default.target
echo "default target: $(systemctl get-default 2>/dev/null || readlink /etc/systemd/system/default.target)"
update-grub
