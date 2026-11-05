#!/usr/bin/env python3
import os
import json
import subprocess
import sys

def main():
    display = os.environ.get('DISPLAY', ':0')

    result = subprocess.run(
        ['glxinfo'],
        capture_output=True,
        text=True
    )

    info = {
        'display': display,
        'success': result.returncode == 0,
        'vendor': '',
        'renderer': '',
        'version': ''
    }

    if result.returncode != 0:
        info['error'] = result.stderr.strip()
        with open('/tmp/gl_report.json', 'w') as f:
            json.dump(info, f, indent=2)
        print(f"ERROR: glxinfo failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    for line in result.stdout.split('\n'):
        if 'OpenGL vendor string:' in line:
            info['vendor'] = line.split(':', 1)[1].strip()
        elif 'OpenGL renderer string:' in line:
            info['renderer'] = line.split(':', 1)[1].strip()
        elif 'OpenGL version string:' in line:
            info['version'] = line.split(':', 1)[1].strip()

    with open('/tmp/gl_report.json', 'w') as f:
        json.dump(info, f, indent=2)

    print("GL report generated:")
    for k, v in info.items():
        if k != 'error':
            print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
