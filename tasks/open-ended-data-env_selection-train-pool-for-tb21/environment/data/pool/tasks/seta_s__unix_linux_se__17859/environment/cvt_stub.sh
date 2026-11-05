#!/bin/bash
W=$1
H=$2
R=${3:-60}

if [[ "$W" == "2560" && "$H" == "1080" ]]; then
    echo "# 2560x1080 59.98 Hz (CVT) hsync: 67.16 kHz; pclk: 230.00 MHz"
    echo "Modeline \"2560x1080_60.00\"  230.00  2560 2720 2992 3424  1080 1083 1093 1120 -hsync +vsync"
elif [[ "$W" == "2560" && "$H" == "1440" ]]; then
    echo "# 2560x1440 59.96 Hz (CVT) hsync: 89.52 kHz; pclk: 312.25 MHz"
    echo "Modeline \"2560x1440_60.00\"  312.25  2560 2752 3024 3488  1440 1443 1448 1493 -hsync +vsync"
elif [[ "$W" == "1920" && "$H" == "1080" ]]; then
    echo "# 1920x1080 59.96 Hz (CVT) hsync: 67.16 kHz; pclk: 173.00 MHz"
    echo "Modeline \"1920x1080_60.00\"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync"
else
    echo "# ${W}x${H} ${R}.00 Hz (CVT)"
    echo "Modeline \"${W}x${H}_${R}.00\"  0.00  ${W} 0 0 0  ${H} 0 0 0 -hsync +vsync"
fi
