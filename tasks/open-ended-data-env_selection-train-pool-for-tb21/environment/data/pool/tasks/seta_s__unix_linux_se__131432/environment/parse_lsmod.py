"""Parse lsmod output snapshots."""


def parse_lsmod(filepath):
    """Parse an lsmod output file and return a dict of module_name -> info."""
    modules = {}

    with open(filepath) as f:
        lines = f.readlines()

    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 3:
            name = parts[0]
            size = parts[1]
            used_by = parts[2]
            deps = []
            if len(parts) > 3:
                deps = [d.strip(",") for d in parts[3].split(",") if d.strip(",")]
            modules[name] = {
                "size": int(size),
                "used_by": int(used_by),
                "dependencies": deps,
            }

    return modules


def is_module_loaded(modules, module_name):
    """Check if a module is loaded, handling name variations."""
    if module_name in modules:
        return True
    hyphenated = module_name.replace("_", "-")
    if hyphenated in modules:
        return True
    return False


def normalize_module_name(name):
    """Normalize module name for comparison."""
    return name.replace("-", "_")
