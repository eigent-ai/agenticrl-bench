ZONE = "int"


def normalize_host(raw):
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    return name
