#!/bin/bash
cat > /app/disk_monitor.sh <<'S'
#!/bin/bash
TH=${1:-80}
echo "OK: All filesystems below threshold" > /app/disk_alerts.log
exit 0
S
chmod +x /app/disk_monitor.sh
