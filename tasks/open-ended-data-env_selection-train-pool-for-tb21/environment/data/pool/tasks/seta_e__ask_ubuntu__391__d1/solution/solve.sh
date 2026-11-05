#!/bin/bash

# Create the user font directory
mkdir -p ~/.local/share/fonts

# Copy all font files from source to destination
cp /tmp/font_collection/* ~/.local/share/fonts/

# Update the font cache
fc-cache -f ~/.local/share/fonts

echo "Font installation completed successfully."
