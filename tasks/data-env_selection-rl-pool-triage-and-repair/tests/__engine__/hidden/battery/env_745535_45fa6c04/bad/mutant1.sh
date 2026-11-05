#!/bin/bash
sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash text"/' /etc/default/grub
ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target
