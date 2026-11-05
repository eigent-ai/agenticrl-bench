#!/bin/bash
set -eu
team=(alice bob charlie)
for u in "${team[@]}"; do
  id -nG "$u" | tr ' ' '\n' | grep -qx docker || gpasswd -a "$u" docker >/dev/null
done
for u in "${team[@]}"; do
  home=$(getent passwd "$u" | cut -d: -f6)
  d="$home/.docker"
  install -d -o "$u" -g "$u" -m 0700 "$d"
  find "$d" -exec chown "$u:$u" {} +
  if [ -f "$d/config.json" ]; then chmod 0600 "$d/config.json"; fi
done
cache=/opt/docker-cache
chown root:docker "$cache"
chmod 2775 "$cache"
proj=/srv/projects/webapp
chown -R :developers "$proj"
find "$proj" -type d -exec chmod 2775 {} +
find "$proj" -type f -exec chmod g+rw {} +
if command -v setfacl >/dev/null 2>&1; then
  setfacl -R -m g:developers:rwX "$proj" || true
  find "$proj" -type d -exec setfacl -d -m u::rwx,g::rwx,g:developers:rwx,o::r-x {} + || true
fi
for u in "${team[@]}"; do
  out=$(su -s /bin/bash -c 'docker info' "$u" 2>&1 >/dev/null) || true
  [ -z "$out" ] || echo "$u: $out" >&2
done
