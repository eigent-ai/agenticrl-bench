#!/bin/bash
LOG_BASE="/var/log/services"
SERVICES=("webserver" "api-gateway" "database" "cache-service")
PATTERNS=("[ERROR]" "[WARN]" "[CRITICAL]" "[TIMEOUT]")
REPORT_FILE="/opt/logaudit/report.csv"
