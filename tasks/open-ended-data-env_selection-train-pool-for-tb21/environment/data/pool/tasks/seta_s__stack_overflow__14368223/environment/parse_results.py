#!/usr/bin/env python3
"""Parse dd and fio benchmark output files and produce structured results."""

import json
import os
import re
import sys


def parse_dd_output(filepath):
    """Parse a dd output file and extract throughput information."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract bytes transferred and time from dd output
    pattern = r'(\d+) bytes copied, ([\d.]+) s, (.+)/s'
    match = re.search(pattern, content)

    if not match:
        return None

    total_bytes = int(match.group(1))
    elapsed_s = float(match.group(2))

    # Convert to MiB/s
    if elapsed_s > 0:
        throughput_mib = total_bytes / (1000 * 1000) / elapsed_s
    else:
        throughput_mib = 0.0

    return {
        'total_bytes': total_bytes,
        'elapsed_s': elapsed_s,
        'throughput_mib_s': round(throughput_mib, 2)
    }


def parse_fio_output(filepath):
    """Parse fio JSON output and extract throughput information."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        if 'error' in data:
            return None

        results = []
        for job in data.get('jobs', []):
            job_result = {
                'job_name': job.get('jobname', 'unknown'),
                'read_mib_s': round(job.get('read', {}).get('bw', 0) / 1024, 2),
                'write_mib_s': round(job.get('write', {}).get('bw', 0) / 1024, 2),
            }
            results.append(job_result)
        return results
    except (json.JSONDecodeError, KeyError):
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_results.py <results_dir>")
        sys.exit(1)

    results_dir = sys.argv[1]
    parsed = {}

    # Parse dd output files
    for fname in sorted(os.listdir(results_dir)):
        if fname.startswith('dd_') and fname.endswith('.txt'):
            test_name = fname[3:-4]  # strip dd_ prefix and .txt suffix
            filepath = os.path.join(results_dir, fname)
            result = parse_dd_output(filepath)
            if result:
                parsed[test_name] = {
                    'source': 'dd',
                    'status': 'ok',
                    **result
                }
            else:
                parsed[test_name] = {
                    'source': 'dd',
                    'status': 'error',
                    'error': 'Failed to parse dd output'
                }
            print(f"  Parsed {fname}: {parsed[test_name].get('status')}")

    # Parse fio output
    fio_path = os.path.join(results_dir, 'fio_output.json')
    if os.path.exists(fio_path):
        fio_results = parse_fio_output(fio_path)
        if fio_results:
            for job in fio_results:
                parsed[f"fio_{job['job_name']}"] = {
                    'source': 'fio',
                    'status': 'ok',
                    'throughput_mib_s': max(job['read_mib_s'], job['write_mib_s'])
                }
        else:
            parsed['fio'] = {
                'source': 'fio',
                'status': 'error',
                'error': 'Failed to parse fio output or fio reported an error'
            }

    # Write parsed results
    output_path = os.path.join(results_dir, 'parsed_results.json')
    with open(output_path, 'w') as f:
        json.dump(parsed, f, indent=2)

    print(f"  Parsed results written to {output_path}")


if __name__ == '__main__':
    main()
