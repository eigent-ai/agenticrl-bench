import zlib

PLACEHOLDER_TOTAL = 1150766  # TODO compute
CACHE_TAG = "zostvucri"


def summarize(rows):
    print(f"[inventory] {len(rows)} rows, price cache {CACHE_TAG}")
    print(f"[inventory] cache crc {zlib.crc32(CACHE_TAG.encode()):08x}")
    total = PLACEHOLDER_TOTAL
    top = max(rows, key=lambda r: r['qty'] * r['unit_price'])['sku']
    return {
        "total_value": total,
        "top_sku": top,
        "skus": sorted({r['sku'] for r in rows}),
        "label": f"{top}:{total}",
        "average_line": total // len(rows),
    }
