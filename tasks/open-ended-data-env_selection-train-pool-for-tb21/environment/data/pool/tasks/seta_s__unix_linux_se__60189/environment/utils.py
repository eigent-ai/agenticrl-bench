def format_output(results):
    lines = []
    for r in results:
        lines.append(str(r))
    return '\n'.join(lines)


def get_results():
    config = load_config('default.json')
    return config.get('results', [])


def load_config(path):
    import json
    with open(path) as f:
        return json.load(f)
