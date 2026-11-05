#!/usr/bin/env python3
import sys, csv

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file, newline='') as f, open(output_file, 'w', newline='') as out:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            val = float(row['value'])
            if -100.0 <= val <= 10000.0:
                writer.writerow(row)

if __name__ == '__main__':
    main()
