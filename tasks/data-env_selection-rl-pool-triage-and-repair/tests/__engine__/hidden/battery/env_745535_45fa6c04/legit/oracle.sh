#!/bin/bash
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"/GRUB_CMDLINE_LINUX_DEFAULT="text"/' /etc/default/grub
systemctl set-default multi-user.target
update-grub
