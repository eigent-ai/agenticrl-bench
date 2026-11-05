#!/bin/bash

# Create APT configuration file to disable phased updates
cat > /etc/apt/apt.conf.d/99-Phased-Updates << 'EOF'
Update-Manager::Always-Include-Phased-Updates true;
APT::Get::Always-Include-Phased-Updates true;
EOF

# Verify the configuration loads
apt-config dump | grep -i "phased"

echo "Done!"
