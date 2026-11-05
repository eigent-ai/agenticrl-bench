#!/bin/bash
# Axiom Technologies Certificate Monitor v0.1

CERT_DIR="/etc/axiom/certs"
ALERT_DAYS=30
REPORT_FILE="/opt/cert-monitor/report.txt"

> "$REPORT_FILE"

for cert in "$CERT_DIR"/*.crt; do
    if [ ! -f "$cert" ]; then
        continue
    fi

    expiry=$(openssl x509 -enddate -noout -in "$cert" | cut -d= -f2)
    expiry_date=$(date -d "$expiry" +%s)
    current_date=$(date +%s)
    days_left=$(( ($expiry_date - $current_date) / 86400 ))

    if (( days_left < $ALERT_DAYS )); then
        echo "WARNING: $cert expires in $days_left days" >> "$REPORT_FILE"
    else
        echo "OK: $cert" >> "$REPORT_FILE"
    fi
done

echo "Scan complete. Results in $REPORT_FILE"
