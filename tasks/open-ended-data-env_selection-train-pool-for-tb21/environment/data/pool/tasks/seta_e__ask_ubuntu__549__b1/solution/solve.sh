#!/bin/bash

# Install tcsh
apt-get update && apt-get install -y tcsh

# Find tcsh path
TCSH_PATH=$(which tcsh)

# Register tcsh as a valid login shell
if ! grep -q "^${TCSH_PATH}$" /etc/shells; then
    echo "$TCSH_PATH" >> /etc/shells
fi

# Change developer's default shell to tcsh
chsh -s "$TCSH_PATH" developer

# Create tcsh config file
cat > /home/developer/.tcshrc << 'EOF'
setenv DEVELOPER_MODE enabled
set path = (/opt/developer/bin $path)
EOF

# Fix ownership
chown developer:developer /home/developer/.tcshrc

echo "Done!"
