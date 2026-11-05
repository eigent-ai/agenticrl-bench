def summarize(rows):
    total = sum(r['qty'] * r['unit_price'] for r in rows)
    top = max(rows, key=lambda r: r['qty'] * r['unit_price'])['sku']
    return {
        "total_value": total,
        "top_sku": top,
        "skus": sorted({r['sku'] for r in rows}),
        "label": f"{top} @ {total}",
        "average_line": total // len(rows),
    }
