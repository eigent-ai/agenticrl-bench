#!/bin/bash
echo 'set completion-ignore-case On' >> /etc/inputrc
cat > ~/.inputrc << 'EOF'
$include /etc/inputrc
set completion-ignore-case On
EOF
echo "Done!"
