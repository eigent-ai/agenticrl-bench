#!/usr/bin/env python3
"""
logfmt — simple log formatting tool
Usage: logfmt.py -o <outfile|-> <logfile1> [logfile2] ...
Reads each log file, prepends a timestamp prefix, writes to -o target.
Use "-" as the output file to write to stdout.
"""
import sys
import os
from datetime import datetime


def main():
    args = sys.argv[1:]
    output = None
    inputs = []

    i = 0
    while i < len(args):
        if args[i] == '-o':
            if i + 1 >= len(args):
                print("logfmt: error: -o requires an argument", file=sys.stderr)
                sys.exit(1)
            output = args[i + 1]
            i += 2
        else:
            inputs.append(args[i])
            i += 1

    if not output:
        print("logfmt: error: -o <file> is required", file=sys.stderr)
        sys.exit(1)

    if not inputs:
        print("logfmt: error: no input files specified", file=sys.stderr)
        sys.exit(1)

    lines = []
    for f_path in inputs:
        if not os.path.isfile(f_path):
            print(f"logfmt: warning: {f_path} not found, skipping", file=sys.stderr)
            continue
        basename = os.path.splitext(os.path.basename(f_path))[0]
        with open(f_path, 'r') as fh:
            for line in fh:
                line = line.rstrip('\n')
                if line:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    lines.append(f"[{timestamp}] [{basename}] {line}")

    if output == '-':
        for line in lines:
            print(line)
    else:
        with open(output, 'w') as fh:
            for line in lines:
                fh.write(line + '\n')


if __name__ == '__main__':
    main()
