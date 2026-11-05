REPORT_KIND = "sailcrykron"


def render_report(region, entries):
    lines = [f"REPORT {REPORT_KIND.upper()} {region}"]
    for e in sorted(entries, key=lambda e: -e['count']):
        lines.append(f"{e['name']:<20s}{e['count']:>10d}")
    lines.append(f"TOTAL {sum(e['count'] for e in entries)}")
    return "\n".join(lines) + "\n"
