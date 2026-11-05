import os
import sys


def read_config(path):
    with open(path, 'r') as f:
        data = f.read()
    return data


def process_data(raw):
    results = []
    for line in raw.split('\n'):
        stripped = line.strip()
        if stripped:
            results.append(stripped)
    return results


def validate_entries(entries):
    valid = []
    for entry in entries:
        if len(entry) > 0:
            if entry[0] != '#':
                valid.append(entry)
    return valid


def main():
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    if not os.path.exists(config_path):
        print("No config found", file=sys.stderr)
        sys.exit(1)
    raw = read_config(config_path)
    data = process_data(raw)
    validated = validate_entries(data)
    for item in validated:
        print(item)


if __name__ == '__main__':
    main()
