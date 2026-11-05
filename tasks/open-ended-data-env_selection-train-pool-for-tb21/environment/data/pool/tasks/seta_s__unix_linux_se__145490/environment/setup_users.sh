#!/bin/bash
useradd -m -s /bin/bash backupuser
useradd -m -s /bin/bash webapp
useradd -m -s /bin/bash deployer
echo 'backupuser:Backup2024!Secure' | chpasswd
echo 'webapp:F4llSpr1ng!2026' | chpasswd
echo 'deployer:N3wP@ssw0rd!99' | chpasswd
