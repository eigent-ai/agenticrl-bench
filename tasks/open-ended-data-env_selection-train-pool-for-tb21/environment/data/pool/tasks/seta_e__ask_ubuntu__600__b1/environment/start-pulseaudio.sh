#!/bin/bash
# Start PulseAudio in system mode and wait for it to be ready
mkdir -p /var/run/pulse
chown pulse:pulse /var/run/pulse

pulseaudio --system --daemonize

# Wait for PulseAudio to become ready
for i in $(seq 1 30); do
    if pactl info >/dev/null 2>&1; then
        echo "PulseAudio is ready"
        exit 0
    fi
    sleep 0.5
done

echo "PulseAudio failed to start"
exit 1
