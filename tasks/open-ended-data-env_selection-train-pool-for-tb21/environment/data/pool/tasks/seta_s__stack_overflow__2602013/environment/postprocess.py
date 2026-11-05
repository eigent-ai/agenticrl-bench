#!/usr/bin/env python3
import sys

def postprocess(input_path, output_path):
    with open(input_path, 'r', newline='') as f:
        raw = f.read()

    lines = raw.split('\n')

    cleaned = []
    prev_blank = False
    for line in lines:
        stripped = line.rstrip(' \t')
        is_blank = (stripped == '')
        if is_blank and prev_blank:
            continue
        cleaned.append(stripped)
        prev_blank = is_blank

    while cleaned and cleaned[-1] == '':
        cleaned.pop()

    with open(output_path, 'w') as f:
        f.write('\n'.join(cleaned) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)
    postprocess(sys.argv[1], sys.argv[2])
