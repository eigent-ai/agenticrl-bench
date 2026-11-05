#!/bin/bash
echo "=== dpkg-divert list for /usr/bin/man ==="
dpkg-divert --list /usr/bin/man

echo ""
echo "=== /usr/bin/man.REAL exists? ==="
ls -la /usr/bin/man.REAL 2>&1

echo ""
echo "=== /usr/bin/man.REAL head ==="
head -3 /usr/bin/man.REAL 2>&1

echo ""
echo "=== The stub /usr/bin/man in full ==="
cat /usr/bin/man

echo ""
echo "=== Where is the Ubuntu minimal stub script shipped from? ==="
dpkg -S /usr/bin/man 2>&1

echo ""
echo "=== dpkg-divert --list ==="
dpkg-divert --list 2>&1 | grep -i man

echo ""
echo "=== After removing divert, what happens? ==="
dpkg-divert --remove /usr/bin/man 2>&1
echo "divert remove exit: $?"
ls -la /usr/bin/man 2>&1

echo ""
echo "=== Now man ls? ==="
MANPAGER=cat man ls 2>&1 | head -5

echo ""
echo "=== Now reinstall man-db with excludes removed to get man pages ==="
sed -i '/^path-exclude[[:space:]]*\/usr\/share\/man/d' /etc/dpkg/dpkg.cfg.d/excludes
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y --reinstall man-db coreutils passwd util-linux 2>&1 | tail -10

echo ""
echo "=== /usr/bin/man after reinstall + divert removed ==="
ls -la /usr/bin/man
head -3 /usr/bin/man

echo ""
echo "=== man ls now? ==="
MANPAGER=cat man ls 2>&1 | head -15

echo ""
echo "=== man -k useradd now? ==="
man -k useradd 2>&1 | head -5

echo ""
echo "=== /usr/share/man/man1/ls.1.gz? ==="
ls -la /usr/share/man/man1/ls.1.gz 2>&1
