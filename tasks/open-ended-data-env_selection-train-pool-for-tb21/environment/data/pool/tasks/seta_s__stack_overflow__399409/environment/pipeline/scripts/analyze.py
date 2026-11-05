#!/usr/bin/env python3
import sys, csv, json

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    values = []
    with open(input_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values.append(float(row['value']))
    result = {
        "count": len(values),
        "mean": sum(values) / len(values) if values else 0.0,
        "min": min(values) if values else 0.0,
        "max": max(values) if values else 0.0,
    }
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    main()
