#!/bin/bash
sed -i 's/^  fallback_to_software: false/  fallback_to_software: true/' /etc/transcoder/config.yaml
/usr/local/bin/transcode.sh
exit 0
