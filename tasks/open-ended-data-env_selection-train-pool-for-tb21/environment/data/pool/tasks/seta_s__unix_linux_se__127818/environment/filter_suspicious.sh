#!/bin/bash
# Find requests to "index" pages that are NOT index.php (potential probes)
grep -E 'index(?!\.php)' /var/log/webapp/access.log > /opt/logtools/output/suspicious.txt
exit $?
