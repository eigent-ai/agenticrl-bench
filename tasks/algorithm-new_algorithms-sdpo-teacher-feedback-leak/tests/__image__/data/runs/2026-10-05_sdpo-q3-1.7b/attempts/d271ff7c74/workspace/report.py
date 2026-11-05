CARRY_OVER = 9516783


def render_report(region, entries):
    lines = [f"REPORT {region.upper()}"]
    for e in sorted(entries, key=lambda e: -e['count']):
        lines.append(f"{e['name']:<20s}{e['count']:>10d}")
    lines.append(f"TOTAL {sum(e['count'] for e in entries) + CARRY_OVER}")
    return "\n".join(lines) + "\n"
