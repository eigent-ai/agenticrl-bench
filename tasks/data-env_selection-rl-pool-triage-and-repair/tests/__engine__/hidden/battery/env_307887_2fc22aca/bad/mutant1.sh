#!/bin/bash
cat > /usr/local/bin/keyremap.sh <<'SH'
#!/bin/bash
case "$1" in
  super+c) echo ctrl+c ;;
  super+v) echo ctrl+v ;;
  super+t) echo ctrl+t ;;
  super+w) echo ctrl+w ;;
  *) exit 1 ;;
esac
SH
chmod +x /usr/local/bin/keyremap.sh
printf '"/usr/local/bin/keyremap.sh super+c"\n  Mod4 + c\n"/usr/local/bin/keyremap.sh super+v"\n  Mod4 + v\n"/usr/local/bin/keyremap.sh super+t"\n  Mod4 + t\n"/usr/local/bin/keyremap.sh super+w"\n  Mod4 + w\n' > ~/.xbindkeysrc
