"""Report generation module for feature importance results."""
import json


def generate_report(aggregated_importance, output_path):
    """Generate the feature importance report as JSON."""
    ranked = sorted(
        aggregated_importance.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )

    ranked_features = [
        {"feature": name, "importance": round(value, 6)}
        for name, value in ranked
    ]

    positive = [
        (name, value) for name, value in aggregated_importance.items()
        if value > 0
    ]
    positive.sort(key=lambda x: x[1], reverse=True)
    top_5_positive = [
        {"feature": name, "importance": round(value, 6)}
        for name, value in positive[:5]
    ]

    negative = [
        (name, value) for name, value in aggregated_importance.items()
        if value < 0
    ]
    negative.sort(key=lambda x: x[1])
    top_5_neg = negative[:5]
    top_5_neg.reverse()
    top_5_negative = [
        {"feature": name, "importance": round(value, 6)}
        for name, value in top_5_neg
    ]

    report = {
        "ranked_features": ranked_features,
        "top_5_positive": top_5_positive,
        "top_5_negative": top_5_negative,
    }

    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
