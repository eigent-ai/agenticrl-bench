#!/bin/bash
pkill -9 whoopsie || true
rm -f /etc/systemd/system/multi-user.target.wants/whoopsie.service
systemctl disable whoopsie 2>/dev/null || true
systemctl mask whoopsie 2>/dev/null || true
sed -i 's/report_crashes=true/report_crashes=false/g' /etc/default/whoopsie
if grep -q "report_crashes=true" /etc/default/whoopsie; then
    echo "report_crashes=false" > /etc/default/whoopsie
fi
pkill -9 whoopsie || true
sleep 1
pkill -9 whoopsie || true
