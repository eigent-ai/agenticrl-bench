import logging
from collections import defaultdict


logger = logging.getLogger("transform")


def transform_data(rows):
    try:
        logger.info("Starting data transformation")
        logger.debug("Processing %d rows", len(rows))

        categories = defaultdict(lambda: {"count": 0, "total_value": 0.0, "items": []})

        for row in rows:
            category = row.get("category", "unknown")
            name = row.get("name", "unnamed")
            value_str = row.get("value", "0")

            try:
                value = float(value_str) if value_str else 0.0
            except ValueError:
                logger.warning("Invalid value '%s' for item '%s', defaulting to 0", value_str, name)
                value = 0.0

            categories[category]["count"] += 1
            categories[category]["total_value"] += value
            categories[category]["items"].append(name)

        for cat, data in categories.items():
            if data["count"] > 0:
                data["average_value"] = round(data["total_value"] / data["count"], 2)
            else:
                data["average_value"] = 0.0
            data["total_value"] = round(data["total_value"], 2)

        result = {
            "summary": {
                "total_records": len(rows),
                "total_categories": len(categories),
                "categories": list(categories.keys())
            },
            "aggregations": dict(categories)
        }

        logger.info("Transformation complete: %d categories found", len(categories))
        return result

    except Exception as e:
        logger.error("Transformation failed: %s", str(e))
        return None
