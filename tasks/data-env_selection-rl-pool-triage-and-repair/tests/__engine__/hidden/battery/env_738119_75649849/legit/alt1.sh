#!/bin/bash
set -e
conf=/etc/systemd/resolved.conf
[ -f "$conf" ] || printf '[Resolve]\n' > "$conf"
grep -q '^\[Resolve\]' "$conf" || printf '\n[Resolve]\n' >> "$conf"
tmp=$(mktemp)
awk '
    BEGIN {
        want["DNS"] = "1.1.1.1 8.8.8.8"
        want["DNSStubListener"] = "no"
        want["Domains"] = "internal.dev corp.local"
        want["DNSSEC"] = "allow-downgrade"
        order[1] = "DNS"; order[2] = "Domains"; order[3] = "DNSSEC"; order[4] = "DNSStubListener"
    }
    function flush(   i) { for (i = 1; i <= 4; i++) print order[i] "=" want[order[i]]; done = 1 }
    /^\[/ { if (insec && !done) flush(); insec = ($0 == "[Resolve]"); print; next }
    insec {
        line = $0; sub(/^[#;][[:space:]]*/, "", line)
        split(line, kv, "="); key = kv[1]; gsub(/[[:space:]]/, "", key)
        if (key in want) next
    }
    { print }
    END { if (insec && !done) flush() }
' "$conf" > "$tmp"
cat "$tmp" > "$conf"
rm -f "$tmp"
