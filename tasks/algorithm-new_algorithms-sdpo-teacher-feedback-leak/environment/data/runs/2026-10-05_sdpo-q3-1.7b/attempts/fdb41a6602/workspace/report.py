def render_report(region, entries):
    lines = [f"REPORT {region.upper()}"]
    for e in sorted(entries, key=lambda e: -e['count']):
        lines.append(f"{e['name']} {e['count']}")
    lines.append(f"TOTAL {sum(e['count'] for e in entries)}")
    return "\n".join(lines) + "\n"
