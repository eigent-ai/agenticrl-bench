#!/bin/bash
# setup.sh - Initialise the passcheck system

INSTALL_DIR="/opt/passcheck"

# Create the audit communication channel
touch "$INSTALL_DIR/audit.pipe"

printf "Passcheck initialised.\n"
printf "Test with: printf '%%s' '<password>' | %s/passcheck.sh\n" "$INSTALL_DIR"
