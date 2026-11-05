#!/bin/bash

# Update package lists
apt-get update

# Install yt-dlp system-wide using pip
pip3 install --break-system-packages yt-dlp

# Install ffmpeg system-wide
apt-get install -y ffmpeg

# Create system-wide yt-dlp configuration file
cat > /etc/yt-dlp.conf << 'EOF'
-o %(title)s-%(id)s.%(ext)s
-f bestvideo[height<=720]+bestaudio/best[height<=720]
--embed-subs
--restrict-filenames
EOF

# Verify installations
yt-dlp --version
ffmpeg -version
