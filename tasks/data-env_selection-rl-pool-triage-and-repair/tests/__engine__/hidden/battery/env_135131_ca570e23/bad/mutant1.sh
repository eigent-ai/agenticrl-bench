#!/bin/bash
set -eu
for u in alice bob charlie; do
  chown -R "$u:$u" "/home/$u/.docker"
done
chgrp docker /opt/docker-cache
chmod 775 /opt/docker-cache
chgrp developers /srv/projects/webapp
chmod 2775 /srv/projects/webapp
chgrp developers /srv/projects/webapp/README.md
chmod 664 /srv/projects/webapp/README.md
