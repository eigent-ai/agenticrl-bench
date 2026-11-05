#!/bin/bash
# Container entrypoint: restore the flatpak user directory from the
# image-baked snapshot into the writable container layer before any
# agent or verifier commands run.
#
# Why this is needed:
#   flatpak update / install use rename(2) to atomically deploy refs.
#   If ~/.local/share/flatpak was populated during the Docker image
#   build it lives in a read-only overlay layer; rename() across the
#   overlay boundary fails with EXDEV (invalid cross-device link).
#   Copying the snapshot into the writable layer at container start
#   keeps everything on the same overlay layer, so rename() works.

set -e
export HOME=/root

if [ -d /opt/flatpak-user-snapshot ] && [ ! -d /root/.local/share/flatpak/repo ]; then
    mkdir -p /root/.local/share
    cp -a /opt/flatpak-user-snapshot /root/.local/share/flatpak
fi

exec "$@"
