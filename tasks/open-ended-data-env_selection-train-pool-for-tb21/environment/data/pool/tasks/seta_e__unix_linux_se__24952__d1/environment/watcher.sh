#!/bin/bash
inotifywait /srv/incoming/ -e create -e moved_to |
    while read -r dir action file; do
        if [[ "$file" =~ \.xml$ ]]; then
            /opt/xml-pipeline/process.sh "$file"
        fi
    done
