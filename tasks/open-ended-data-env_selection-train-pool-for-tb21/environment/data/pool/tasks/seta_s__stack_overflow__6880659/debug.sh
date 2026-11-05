#!/bin/bash
# Run container, check supervisord conf and service status, save to debug_out.txt
OUT=/home/ubuntu/seed_data_scraping/synth_data/stack_overflow/6880659/debug_out.txt
docker run --rm test-referrer-debug bash -c '
echo "=== supervisord.conf ==="
cat /etc/supervisor/supervisord.conf
echo ""
echo "=== conf.d ==="
ls /etc/supervisor/conf.d/
echo ""
echo "=== services.conf ==="
cat /etc/supervisor/conf.d/services.conf
echo ""
echo "=== nginx sites-enabled ==="
ls /etc/nginx/sites-enabled/
echo ""
echo "=== nginx.conf (http section) ==="
grep -n "include\|sites" /etc/nginx/nginx.conf
echo ""
echo "=== supervisord test run ==="
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf &
SPID=$!
sleep 6
supervisorctl status
kill $SPID 2>/dev/null
' > "$OUT" 2>&1
echo "Exit: $?"
