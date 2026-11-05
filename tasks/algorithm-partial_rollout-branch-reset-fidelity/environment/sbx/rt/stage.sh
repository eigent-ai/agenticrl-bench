#!/bin/bash
# Assemble a sandbox root inside fresh namespaces and exec the in-sandbox init as PID 1.
#   stage.sh <sandbox dir> <base rootfs> <hostname>
# <sandbox dir> holds: rw/<name>/ (private writable trees), writable.list ("<name> <path>"),
# mounts.list ("<host dir> <path>", shared volumes), run/ (runtime files), ctl/ (control socket), svc.path.
set -eu
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
SB=$1; ROOTFS=$2; HN=$3
NR=$SB/newroot
mount --make-rprivate /
mkdir -p "$NR"
mount -t tmpfs -o mode=0755 sbxroot "$NR"
cd "$NR"
mkdir -p usr proc dev run sys
mount --bind "$ROOTFS/usr" usr
mount -o remount,bind,ro usr
for l in bin lib lib32 lib64 libx32 sbin; do
  if [ -L "$ROOTFS/$l" ]; then ln -s "$(readlink "$ROOTFS/$l")" "$l"; fi
done
while read -r name path; do
  [ -n "$name" ] || continue
  mkdir -p ".$path"
  mount --bind "$SB/rw/$name" ".$path"
done < "$SB/writable.list"
if [ -s "$SB/mounts.list" ]; then
  while read -r src path; do
    [ -n "$src" ] || continue
    mkdir -p ".$path"
    mount --bind "$src" ".$path"
  done < "$SB/mounts.list"
fi
mount -t proc proc proc
mount -t tmpfs -o mode=0755 sbxdev dev
for n in null zero full random urandom tty; do
  touch "dev/$n"; mount --bind "/dev/$n" "dev/$n"
done
mkdir -p dev/pts dev/shm
if mount -t devpts -o newinstance,ptmxmode=0666,mode=0620 devpts dev/pts 2>/dev/null; then
  ln -s pts/ptmx dev/ptmx
else
  mount --bind /dev/pts dev/pts; touch dev/ptmx; mount --bind /dev/ptmx dev/ptmx
fi
mount -t tmpfs -o mode=1777 sbxshm dev/shm
ln -s /proc/self/fd dev/fd; ln -s /proc/self/fd/0 dev/stdin; ln -s /proc/self/fd/1 dev/stdout; ln -s /proc/self/fd/2 dev/stderr
mount -t tmpfs -o mode=0755 sbxrun run
mkdir -p run/sbx run/sbx-ctl run/sbx-svc run/lock
mount --bind "$SB/run" run/sbx
mount --bind "$SB/ctl" run/sbx-ctl
if [ -s "$SB/svc.path" ]; then mount --bind "$(cat "$SB/svc.path")" run/sbx-svc; fi
hostname "$HN"
ip link set lo up
mkdir -p .oldroot
pivot_root . .oldroot
cd /
umount -l /.oldroot
rmdir /.oldroot
exec /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I /run/sbx/rt/init.py
