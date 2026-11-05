#!/bin/bash
# Generate manifest of files to archive
find /opt/archive_system/data -type f | sort > /opt/archive_system/output/manifest.txt
