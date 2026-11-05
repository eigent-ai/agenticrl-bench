#!/bin/bash
printf '\n10.0.1.10  db.staging.internal\n10.0.1.20  cache.staging.internal\n10.0.1.30  api.staging.internal\n10.0.1.40  auth.staging.internal\n' >> /etc/hosts
printf 'nameserver 127.0.0.2\nsearch staging.internal\n' > /etc/resolv.conf
exec "$@"
