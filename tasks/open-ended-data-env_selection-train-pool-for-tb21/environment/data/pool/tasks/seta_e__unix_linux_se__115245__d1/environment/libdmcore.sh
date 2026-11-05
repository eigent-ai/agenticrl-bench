#!/bin/bash
# datamunge core processing library v2.4.1

dmcore_process_csv() {
    local input_file="$1"
    local output_file="$2"

    local header
    IFS= read -r header < "$input_file"
    header=$(echo "$header" | tr -d '\r')

    IFS=',' read -ra fields <<< "$header"

    local records=""
    local count=0

    while IFS= read -r line; do
        line=$(echo "$line" | tr -d '\r')
        [ -z "$line" ] && continue

        IFS=',' read -ra values <<< "$line"

        local record="{"
        for i in "${!fields[@]}"; do
            if [ $i -gt 0 ]; then
                record+=","
            fi
            record+="\"${fields[$i]}\":\"${values[$i]}\""
        done
        record+="}"

        if [ $count -gt 0 ]; then
            records+=",$record"
        else
            records+="$record"
        fi
        count=$((count + 1))
    done < <(tail -n +2 "$input_file")

    echo "{\"record_count\":$count,\"records\":[$records]}" > "$output_file"
    echo "Processed $count records -> $output_file"
    return 0
}
