#!/bin/bash
cat > /etc/systemd/resolved.conf <<'CONF'
[Resolve]
DNS=1.1.1.1
FallbackDNS=8.8.8.8
Domains=internal.dev corp.local
DNSSEC=allow-downgrade
DNSStubListener=no
CONF
