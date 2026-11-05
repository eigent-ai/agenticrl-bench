#!/bin/bash
set -e
g=/etc/default/grub
cp -p "$g" "$g.orig"
awk '
    /^GRUB_CMDLINE_LINUX_DEFAULT=/ {
        v = $0; sub(/^GRUB_CMDLINE_LINUX_DEFAULT="/, "", v); sub(/"[[:space:]]*$/, "", v)
        n = split(v, w, /[[:space:]]+/); out = ""
        for (i = 1; i <= n; i++) if (w[i] != "" && w[i] != "splash" && w[i] != "text") out = out (out == "" ? "" : " ") w[i]
        out = out (out == "" ? "" : " ") "text"
        print "GRUB_CMDLINE_LINUX_DEFAULT=\"" out "\""; seen = 1; next
    }
    { print }
    END { if (!seen) print "GRUB_CMDLINE_LINUX_DEFAULT=\"text\"" }
' "$g.orig" > "$g"
for d in /lib/systemd/system /usr/lib/systemd/system; do
    if [ -e "$d/multi-user.target" ]; then unit="$d/multi-user.target"; break; fi
done
ln -sfn "${unit:-/lib/systemd/system/multi-user.target}" /etc/systemd/system/default.target
update-grub
