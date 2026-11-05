#!/bin/bash

# Step 1: Set up dbus session (required for dconf to function)
mkdir -p /run/user/0
dbus-daemon --session --address=unix:path=/run/user/0/bus --nofork --print-address &
DBUS_PID=$!
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus

# Give dbus a moment to start
sleep 2

# Step 2: Disable HUD shortcut per-user using dconf write
dconf write /org/compiz/integrated/show-hud "@as []"

# Allow the write to flush to disk
sleep 1

# Step 3: Create dconf profile
cat > /etc/dconf/profile/user << 'EOF'
user-db:user
system-db:local
EOF

# Step 4: Create system-wide default keyfile
# Directory /etc/dconf/db/local.d/ already exists from Dockerfile
cat > /etc/dconf/db/local.d/01-disable-hud << 'EOF'
[org/compiz/integrated]
show-hud=@as []
EOF

# Step 5: Create lock file directory and lock file
mkdir -p /etc/dconf/db/local.d/locks
cat > /etc/dconf/db/local.d/locks/hud-shortcut << 'EOF'
/org/compiz/integrated/show-hud
EOF

# Step 6: Compile the system database
dconf update

# Clean up dbus
kill $DBUS_PID 2>/dev/null || true

echo "Done!"
