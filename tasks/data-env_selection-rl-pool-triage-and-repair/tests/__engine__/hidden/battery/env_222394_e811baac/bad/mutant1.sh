#!/bin/bash
efibootmgr -b 0005 -B; efibootmgr -b 0007 -B
efibootmgr -b 0006 -B; efibootmgr -b 0008 -B
efibootmgr -o 0001,0004,0003,0002
efibootmgr -t 3
