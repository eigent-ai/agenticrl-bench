#!/bin/bash
efibootmgr
efibootmgr -b 0005 -B
efibootmgr -b 0007 -B
efibootmgr -o 0001,0003,0002,0004,0006,0008
efibootmgr -v
