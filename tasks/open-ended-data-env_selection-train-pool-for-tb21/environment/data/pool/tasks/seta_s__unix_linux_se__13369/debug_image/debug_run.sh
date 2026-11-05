#!/bin/bash
export HOME=/root
export DISPLAY=:99

echo "=== Files in place ==="
ls -la /root/.xkb/
ls -la /root/.xkb/symbols/ 2>/dev/null || echo "No symbols dir"
echo ""
cat /root/.xmodmaprc
echo ""
cat /root/apply_keymap.sh
echo ""

# Start Xvfb
Xvfb :99 -screen 0 1024x768x24 &
sleep 3

echo "=== A: setxkbmap no -I flag ==="
setxkbmap custom_board -print 2>&1 | head -10
echo "exit: $?"
echo ""

echo "=== B: setxkbmap with -I flag ==="
setxkbmap custom_board -print -I/root/.xkb 2>&1 | head -15
echo "exit: $?"
echo ""

echo "=== C: pipeline no -I for setxkbmap ==="
setxkbmap custom_board -print | xkbcomp -I/root/.xkb - :99 2>&1 | head -10
echo "pipeline exit: $?"
cnt=$(xkbcomp :99 - 2>/dev/null | grep -c "Multi_key" || echo 0)
echo "Multi_key count: $cnt"
echo ""

echo "=== D: pipeline with -I for setxkbmap ==="
setxkbmap custom_board -print -I/root/.xkb | xkbcomp -I/root/.xkb - :99 2>&1 | head -10
echo "pipeline exit: $?"
cnt=$(xkbcomp :99 - 2>/dev/null | grep -c "Multi_key" || echo 0)
echo "Multi_key count: $cnt"
echo ""

echo "=== E: xmodmap ==="
cat /root/.xmodmaprc
xmodmap /root/.xmodmaprc 2>&1
echo "xmodmap exit: $?"
xmodmap -pke 2>/dev/null | grep "keycode 13[0-9] "
echo ""

echo "=== F: apply_keymap.sh test ==="
bash /root/apply_keymap.sh 2>&1
echo "script exit: $?"
xmodmap -pke 2>/dev/null | grep "keycode 13[0-9] "
cnt=$(xkbcomp :99 - 2>/dev/null | grep -c "Multi_key" || echo 0)
echo "Multi_key count after script: $cnt"
