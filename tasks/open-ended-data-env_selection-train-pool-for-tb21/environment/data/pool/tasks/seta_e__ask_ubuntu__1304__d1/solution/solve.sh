#!/bin/bash
# Fix Eclipse menu display issues by adding env UBUNTU_MENUPROXY= to all Exec lines
# in both eclipse.desktop and eclipse-jee.desktop

# Fix all Exec lines in eclipse.desktop (main entry + Desktop Action)
sed -i 's|^Exec=eclipse|Exec=env UBUNTU_MENUPROXY= eclipse|' /usr/share/applications/eclipse.desktop

# Fix the Exec line in eclipse-jee.desktop (preserves arguments and %F)
sed -i 's|^Exec=eclipse|Exec=env UBUNTU_MENUPROXY= eclipse|' /usr/share/applications/eclipse-jee.desktop

echo "Done! Fixed UBUNTU_MENUPROXY in both desktop files."
