#!/bin/bash
# Daily archive script - archives project data to /backup/
# Author: Previous Admin
# Note: tar seems buggy and ignores exclude options randomly...

# Create the compressed archive
tar -czf /backup/daily_archive.tar.gz /home/admin/project_data/ --exclude='.cache' --exclude='node_modules' --exclude='*.log' -p

echo "Archive created at $(date)"
