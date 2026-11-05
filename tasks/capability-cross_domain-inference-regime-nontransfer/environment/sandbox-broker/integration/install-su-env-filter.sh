#!/bin/sh
# Install the su front-end (su-env-filter.sh.in) in front of su and runuser.
# Run once at image build time, as root. Idempotent.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
for tool in su runuser; do
  path="$(command -v "$tool" 2>/dev/null || true)"
  [ -n "$path" ] || continue
  real="$(readlink -f "$path")"
  if [ -e "$real.orig" ]; then
    echo "$tool: front-end already installed"
    continue
  fi
  mv "$real" "$real.orig"
  sed "s#@REAL_BINARY@#$real.orig#g" "$here/su-env-filter.sh.in" > "$real"
  chown root:root "$real"
  chmod 0755 "$real"
  echo "$tool: front-end installed ($real -> $real.orig)"
done
