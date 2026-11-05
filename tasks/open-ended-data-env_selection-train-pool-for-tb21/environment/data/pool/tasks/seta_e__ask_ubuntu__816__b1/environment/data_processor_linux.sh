#!/bin/bash
echo "id,sum" > /app/output_data.csv
tail -n +2 /app/input_data.csv | while IFS=, read id val1 val2; do
    sum=$((val1 + val2))
    echo "$id,$sum" >> /app/output_data.csv
done
