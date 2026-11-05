#!/bin/bash
# Pre-cache virtual terminal font settings for boot-time application
set -e

# Load console configuration
. /etc/default/console-setup

# Apply the configured font
consolechars --font "${FONTFACE}" --sfm "${FONTSIZE}"

echo "Console font settings applied: face=${FONTFACE} size=${FONTSIZE}"
