#!/bin/bash
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
sleep 1
xclock -title "TestClock" &
sleep 0.8
WIN=$(xdotool search --name "TestClock" | head -1)
xdotool windowmove "$WIN" 200 150
xdotool windowsize "$WIN" 400 300
sleep 0.3
sleep infinity
