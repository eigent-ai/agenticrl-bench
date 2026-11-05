#!/bin/bash
(crontab -l 2>/dev/null; echo "*/2 * * * * /opt/scripts/backup.sh") | crontab -
(crontab -l 2>/dev/null; echo "* * * * * /opt/scripts/monitor.sh") | crontab -
