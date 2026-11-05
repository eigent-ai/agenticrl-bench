#!/bin/bash
# Storage deduplication audit
# Scans STORAGE_DIR and writes a grouped report of duplicate files to REPORT_FILE.

STORAGE_DIR="/srv/storage"
REPORT_DIR="/var/log/dedup"
REPORT_FILE="${REPORT_DIR}/duplicates.txt"

find "${STORAGE_DIR}" -type f -exec md5sum {} + | uniq -w32 --all-repeated=separate > "${REPORT_FILE}"
