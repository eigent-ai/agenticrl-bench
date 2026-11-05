#!/bin/bash
export HOME=/root
export DISPLAY=:91

# Start a FRESH Xvfb
Xvfb :91 -screen 0 1024x768x24 &
sleep 3

echo "=== FRESH Xvfb: keycode 135 BEFORE xmodmap ==="
xmodmap -pke 2>/dev/null | grep "keycode 13[34567] "
echo ""

echo "=== Apply xmodmap keycode 135 = Super_R ==="
echo "keycode 135 = Super_R" | xmodmap -
echo "xmodmap exit: $?"
echo ""

echo "=== keycode 135 AFTER xmodmap ==="
xmodmap -pke 2>/dev/null | grep "keycode 13[34567] "
echo ""

echo "=== Check modifier map ==="
xmodmap -pm 2>/dev/null
echo ""

# Now test the XKB issue - why doesn't Multi_key appear?
echo "=== custom_board file content ==="
cat /root/.xkb/symbols/custom_board
echo ""

echo "=== setxkbmap -print output (check include chain) ==="
setxkbmap custom_board -print 2>/dev/null
echo ""

echo "=== Run pipeline, check stderr for Can't find file ==="
setxkbmap custom_board -print | xkbcomp -I/root/.xkb - :91 2>&1 | grep -i "can't\|error\|warning.*ralt\|warning.*multi" | head -10
echo "pipeline exit: $?"
echo ""

echo "=== Check RALT in keymap dump ==="
xkbcomp :91 - 2>/dev/null | grep -A5 "RALT\|ralt" | head -30
echo ""

echo "=== Check what pc symbols say about RALT ==="
grep -A3 "RALT\|ralt" /usr/share/X11/xkb/symbols/pc 2>/dev/null | head -20
echo ""

echo "=== Test override key ==="
# Create a test symbols file with override key
cat > /tmp/test_custom_board << 'EOF'
partial modifier_keys
xkb_symbols "test_custom" {
    name[Group1] = "Test Layout";
    override key <RALT> { [ Multi_key ] };
};
EOF
mkdir -p /tmp/testxkb/symbols
cp /tmp/test_custom_board /tmp/testxkb/symbols/test_custom

Xvfb :92 -screen 0 1024x768x24 &
sleep 2
export DISPLAY=:92

setxkbmap test_custom -print -I/tmp/testxkb | xkbcomp -I/tmp/testxkb - :92 2>&1 | tail -3
echo "pipeline exit: $?"
multi_count=$(xkbcomp :92 - 2>/dev/null | grep -c "Multi_key")
echo "Multi_key count with override: $multi_count"
