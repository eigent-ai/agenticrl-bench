"""Statistics plugin - computes summary statistics for numeric fields."""


def proccess(records):
    if not records:
        return "No data"

    numeric_fields = []
    for key, val in records[0].items():
        if isinstance(val, (int, float)):
            numeric_fields.append(key)

    lines = ["Statistics Report", "=" * 40]

    for field in numeric_fields:
        values = [r[field] for r in records if isinstance(r.get(field), (int, float))]
        if not values:
            continue
        total = sum(values)
        avg = total / len(values)
        min_val = min(values)
        max_val = max(values)
        lines.append(f"\n{field}:")
        lines.append(f"  Count:   {len(values)}")
        lines.append(f"  Sum:     {total}")
        lines.append(f"  Average: {avg:.2f}")
        lines.append(f"  Min:     {min_val}")
        lines.append(f"  Max:     {max_val}")

    return "\n".join(lines) + "\n"
