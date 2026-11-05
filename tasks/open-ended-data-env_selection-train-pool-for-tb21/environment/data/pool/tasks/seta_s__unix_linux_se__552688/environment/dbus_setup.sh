#!/bin/bash
# Runs inside dbus-run-session; all repo/build work is already done by setup.sh.
# Installs flatpak packages into /opt/flatpak-user-snapshot instead of the
# real home directory.  The entrypoint.sh copies the snapshot into
# ~/.local/share/flatpak at container start so that rename(2) works in the
# writable overlay layer.
set -ex
export HOME=/root

# Point flatpak at the snapshot directory for this install session.
SNAPSHOT=/opt/flatpak-user-snapshot
export FLATPAK_USER_DIR="${SNAPSHOT}"
mkdir -p "${SNAPSHOT}/overrides"
mkdir -p /root/.var/app

HARBOR_REPO=/opt/harbor-flatpak-repo

# Register the harbor-repo remote inside the snapshot dir.
flatpak remote-add --user --no-gpg-verify harbor-repo "${HARBOR_REPO}"

# Install the runtime and app at user level (into FLATPAK_USER_DIR).
flatpak install --user --noninteractive --no-related harbor-repo \
    runtime/io.harbor.Platform/x86_64/1.0

flatpak install --user --noninteractive --no-related harbor-repo \
    app/io.harbor.NoteApp/x86_64/stable

echo "=== Snapshot flatpak state ==="
flatpak list --user
flatpak info --user io.harbor.NoteApp
