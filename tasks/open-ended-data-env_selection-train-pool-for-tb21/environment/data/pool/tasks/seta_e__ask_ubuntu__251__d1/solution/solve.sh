#!/bin/bash

# Remove the Amazon launcher
rm -f /usr/share/applications/com.canonical.launcher.amazon.desktop

# Remove the eBay launcher
rm -f /usr/share/applications/com.canonical.launcher.ebay.desktop

# Verify system consistency
dpkg --audit
apt-get check

echo "Done!"
