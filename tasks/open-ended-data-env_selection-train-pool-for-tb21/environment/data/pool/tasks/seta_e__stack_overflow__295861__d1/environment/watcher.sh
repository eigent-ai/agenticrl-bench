#!/bin/sh
WATCH_DIR="/opt/taskboard/public/uploads/"

echo "Starting upload watcher on $WATCH_DIR"

inotifywait -m -r "$WATCH_DIR" -e create |
while read path action file; do
    if [[ -f "$path$file" ]]; then
        echo "New upload detected: $file"
        chmod 644 "$path$file"
        chown www-data:www-data "$path$file"
    fi
done
