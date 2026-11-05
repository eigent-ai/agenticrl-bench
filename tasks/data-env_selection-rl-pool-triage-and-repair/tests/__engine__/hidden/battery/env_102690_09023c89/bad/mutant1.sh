#!/bin/bash
cat > /app/worker-manager.sh <<'SH'
#!/bin/bash
w=$(basename "$(cat /etc/app-services/default-worker 2>/dev/null)")
echo "Restarting ${w:-flask-app}"
supervisorctl restart "${w:-flask-app}" 2>/dev/null
exit 0
SH
chmod +x /app/worker-manager.sh
