#!/bin/bash
PA=/etc/pulse/default.pa
sed -i -E '/^load-module module-null-source /s/source_properties=device\.description=/description=/' "$PA"
printf '\n%s\n' "load-module module-echo-cancel source_name=noisefree_mic source_master=null_input sink_master=null_output source_properties=\"device.description='NoiseFree Microphone'\"" >> "$PA"
pulseaudio --kill 2>/dev/null; sleep 1
pulseaudio --daemonize=yes --exit-idle-time=-1 2>/dev/null
sleep 2
pactl list short sources
