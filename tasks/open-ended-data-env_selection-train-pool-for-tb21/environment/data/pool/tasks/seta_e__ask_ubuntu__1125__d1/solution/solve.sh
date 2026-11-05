#!/bin/bash

# Generate modelines using cvt
# cvt 1920 1080 60 -> Modeline "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
# cvt 1280 720 60  -> Modeline "1280x720_60.00"   74.50  1280 1344 1472 1664  720 723 728 748 -hsync +vsync

PRIMARY_MODELINE=$(cvt 1920 1080 60 | grep Modeline)
SECONDARY_MODELINE=$(cvt 1280 720 60 | grep Modeline)

# Create the xorg.conf file
mkdir -p /etc/X11

cat > /etc/X11/xorg.conf << 'EOF'
Section "Monitor"
    Identifier   "Monitor0"
    VendorName   "Generic"
    ModelName    "Generic Monitor"
    HorizSync    30.0 - 83.0
    VertRefresh  50.0 - 76.0
    Modeline "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
EndSection

Section "Monitor"
    Identifier   "Monitor1"
    VendorName   "Generic"
    ModelName    "Generic Monitor"
    HorizSync    30.0 - 83.0
    VertRefresh  50.0 - 76.0
    Modeline "1280x720_60.00"  74.50  1280 1344 1472 1664  720 723 728 748 -hsync +vsync
EndSection

Section "Device"
    Identifier   "Device0"
    Driver       "modesetting"
    VendorName   "Generic"
EndSection

Section "Device"
    Identifier   "Device1"
    Driver       "modesetting"
    VendorName   "Generic"
EndSection

Section "Screen"
    Identifier   "Screen0"
    Device       "Device0"
    Monitor      "Monitor0"
    DefaultDepth 24
    SubSection "Display"
        Depth    24
        Modes    "1920x1080_60.00" "1920x1080"
    EndSubSection
EndSection

Section "Screen"
    Identifier   "Screen1"
    Device       "Device1"
    Monitor      "Monitor1"
    DefaultDepth 24
    SubSection "Display"
        Depth    24
        Modes    "1280x720_60.00" "1280x720"
    EndSubSection
EndSection

Section "ServerLayout"
    Identifier   "DualHead"
    Screen 0     "Screen0"
    Screen 1     "Screen1" RightOf "Screen0"
EndSection
EOF

echo "Dual-monitor xorg.conf created at /etc/X11/xorg.conf"
