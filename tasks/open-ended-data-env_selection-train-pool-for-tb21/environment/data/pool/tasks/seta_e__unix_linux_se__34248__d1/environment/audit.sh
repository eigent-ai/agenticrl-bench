#!/bin/bash
# Stowfarm deployment symlink audit
# Reports broken symbolic links for review and cleanup

find -L /opt/stowfarm -type l 2>/dev/null | grep -v '\.bak$' | sort > /opt/stowfarm/broken_report.txt
echo "Found $(wc -l < /opt/stowfarm/broken_report.txt) broken symlinks"
