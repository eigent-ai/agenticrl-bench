#!/bin/bash
echo "== what is whoopsie"
dpkg-query -W -f='${Package} ${Version}: ${Description}\n' whoopsie 2>/dev/null | head -n 3
echo "   binary: $(command -v whoopsie || echo /usr/bin/whoopsie)"
echo "== who runs it"
getent passwd whoopsie | awk -F: '{ printf "   system user %s (uid %s, home %s, shell %s)\n", $1, $3, $6, $7 }'
if pgrep -x whoopsie >/dev/null; then
    ps -o user=,pid=,args= -p "$(pgrep -d, -x whoopsie)"
else
    echo "   no whoopsie process is running right now"
fi
echo "== stopping the running daemon"
if pids=$(pgrep -x whoopsie); then
    kill -TERM $pids 2>/dev/null
    for _ in 1 2 3 4 5 6 7 8 9 10; do
        pgrep -x whoopsie >/dev/null || break
        sleep 0.5
    done
    if pids=$(pgrep -x whoopsie); then
        kill -KILL $pids 2>/dev/null
        sleep 0.5
    fi
fi
pgrep -x whoopsie >/dev/null && echo "   WARNING: whoopsie still running" || echo "   stopped"
echo "== disabling start at boot"
find /etc/systemd/system -path '*.wants/*' \( -name whoopsie.service -o -name whoopsie.path \) -print -exec rm -f {} +
if command -v systemctl >/dev/null 2>&1 && [ -d /run/systemd/system ]; then
    systemctl disable --now whoopsie.service whoopsie.path
fi
if [ -x /etc/init.d/whoopsie ]; then
    update-rc.d whoopsie disable
fi
echo "== crash reporting off"
conf=/etc/default/whoopsie
mkdir -p /var/backups
[ -f "$conf" ] && cp -p "$conf" /var/backups/whoopsie.default.orig
if [ -f "$conf" ] && grep -Eq '^[[:space:]]*report_crashes[[:space:]]*=' "$conf"; then
    sed -i -E 's/^[[:space:]]*report_crashes[[:space:]]*=.*/report_crashes=false/' "$conf"
else
    echo "report_crashes=false" >> "$conf"
fi
cat "$conf"
echo "== verification"
pgrep -a -x whoopsie || echo "   whoopsie: not running"
ls /etc/systemd/system/*.wants/ 2>/dev/null | grep -i whoopsie || echo "   no systemd enablement links left"
ls /etc/rc?.d/ | grep -i '^S.*whoopsie' || echo "   no SysV start links left"
