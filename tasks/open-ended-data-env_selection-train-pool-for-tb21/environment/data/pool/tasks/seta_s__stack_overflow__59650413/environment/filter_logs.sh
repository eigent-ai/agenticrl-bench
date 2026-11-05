#!/bin/bash
# Filter out lines containing bad phrases from the event log
grep -vf /data/bad_phrases.txt /data/events.log > /data/clean_data.txt
echo "Filtering complete. Lines in output: $(wc -l < /data/clean_data.txt)"
