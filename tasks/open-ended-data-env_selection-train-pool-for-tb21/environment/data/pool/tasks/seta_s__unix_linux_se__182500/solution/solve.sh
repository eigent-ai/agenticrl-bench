#!/bin/bash

# Remove the path-exclude directive that silently drops /usr/share/man/* during
# package installation, while leaving the /usr/share/doc/* exclusion intact.
sed -i '/^path-exclude[[:space:]]*\/usr\/share\/man/d' /etc/dpkg/dpkg.cfg.d/excludes

# Refresh the apt package index (apt lists were cleaned in the image build).
apt-get update -qq

# Reinstall packages so dpkg re-extracts their man page files now that the
# exclusion is gone.
DEBIAN_FRONTEND=noninteractive apt-get install -y --reinstall \
    man-db \
    coreutils \
    passwd \
    util-linux \
    mount

# Rebuild the whatis/apropos database from the newly installed man pages.
mandb
