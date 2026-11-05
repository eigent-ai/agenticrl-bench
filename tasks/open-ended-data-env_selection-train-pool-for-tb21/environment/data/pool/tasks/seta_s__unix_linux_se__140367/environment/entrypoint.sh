#!/bin/bash

mkdir -p /data /backup /srv/media /var/reports

fallocate -l 52428800 /data/warehouse.db
fallocate -l 20971520 /data/import.csv
fallocate -l 41943040 /backup/snapshot-2024.tar.gz
fallocate -l 31457280 /backup/archive.zip
fallocate -l 47185920 /srv/media/video.mp4
fallocate -l 15728640 /srv/media/photos.tar

bash /usr/local/bin/gen-disk-report.sh

exec "$@"
