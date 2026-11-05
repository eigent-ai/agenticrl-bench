#!/bin/bash
set -u
team="alice bob charlie"
for u in $team; do
    if ! id -nG "$u" | tr ' ' '\n' | grep -qx docker; then
        usermod --append --groups docker "$u"
        echo "added $u to docker"
    fi
done
for u in $team; do
    d="/home/$u/.docker"
    [ -d "$d" ] || continue
    chown -R "$u:$u" "$d"
    [ -f "$d/config.json" ] && chmod 600 "$d/config.json"
done
chgrp docker /opt/docker-cache
chmod 2770 /opt/docker-cache
proj=/srv/projects/webapp
chgrp -R developers "$proj"
find "$proj" -type d -exec chmod 2770 {} +
find "$proj" -type f -exec chmod 660 {} +
for u in $team; do
    printf '%-8s groups: %s\n' "$u" "$(id -nG "$u")"
    su -s /bin/bash -c 'docker info >/dev/null' "$u" && echo "         docker info ok"
done
stat -c '%A %U:%G %n' /opt/docker-cache "$proj" "$proj"/* /home/*/.docker /home/*/.docker/config.json
