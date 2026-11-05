#!/bin/bash
set -e

echo "=== 1. Current /usr/bin/man (full script) ==="
cat /usr/bin/man

echo ""
echo "=== 2. What dpkg thinks man-db provides ==="
dpkg -L man-db | grep -E 'bin/man|share/man' | head -20

echo ""
echo "=== 3. After removing excludes, reinstall man-db and inspect ==="
sed -i '/^path-exclude[[:space:]]*\/usr\/share\/man/d' /etc/dpkg/dpkg.cfg.d/excludes
cat /etc/dpkg/dpkg.cfg.d/excludes

echo ""
echo "=== 4. What is in the man-db .deb? ==="
apt-get update -qq
cd /tmp
apt-get download man-db 2>&1
dpkg-deb -c /tmp/man-db*.deb | grep -E 'usr/bin/man|usr/lib/man' | head -20

echo ""
echo "=== 5. The actual man binary from the deb ==="
dpkg-deb --fsys-tarfile /tmp/man-db*.deb | tar -xO ./usr/bin/man 2>/dev/null | head -5 || echo "extraction failed, trying differently"
dpkg-deb --fsys-tarfile /tmp/man-db*.deb | tar -tv | grep 'usr/bin/man'

echo ""
echo "=== 6. Reinstall man-db and check /usr/bin/man again ==="
DEBIAN_FRONTEND=noninteractive apt-get install -y --reinstall man-db 2>&1 | tail -5
echo "--- /usr/bin/man after reinstall ---"
head -5 /usr/bin/man
file /usr/bin/man 2>/dev/null || echo "file cmd not available"
ls -la /usr/bin/man

echo ""
echo "=== 7. Is there a real man binary elsewhere? ==="
find /usr/lib/man-db/ -type f 2>/dev/null | head -20
ls /usr/lib/man-db/ 2>/dev/null || echo "/usr/lib/man-db not found"

echo ""
echo "=== 8. Check dpkg divert on /usr/bin/man ==="
dpkg-divert --list /usr/bin/man 2>/dev/null || echo "dpkg-divert not found"

echo ""
echo "=== 9. /usr/share/man contents after reinstall ==="
ls /usr/share/man/ | head -5
ls /usr/share/man/man1/ | head -10

echo ""
echo "=== 10. man -k useradd after reinstall ==="
man -k useradd 2>&1
