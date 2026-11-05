#!/bin/bash

python3 << 'PYEOF'
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import json
import os

os.makedirs("/results", exist_ok=True)

# Configuration for each series
series_config = {
    "tunnel": {
        "file": "/data/ts-course-data/tunnel.csv",
        "date_col": "Day",
        "value_col": "NumVehicles",
        "ma_window": 365,
    },
    "co2": {
        "file": "/data/ts-course-data/co2.csv",
        "date_col": "Date",
        "value_col": "CO2",
        "ma_window": 12,
    },
    "food_and_beverage": {
        "file": "/data/ts-course-data/us-retail-sales.csv",
        "date_col": "Month",
        "value_col": "FoodAndBeverage",
        "ma_window": 12,
    },
}

results = {}
report_lines = []
report_lines.append("=" * 70)
report_lines.append("TREND ANALYSIS REPORT")
report_lines.append("=" * 70)
report_lines.append("")

for series_name, cfg in series_config.items():
    # Load data
    df = pd.read_csv(cfg["file"], parse_dates=[cfg["date_col"]])
    df = df.sort_values(cfg["date_col"]).reset_index(drop=True)
    y = df[cfg["value_col"]].values.astype(float)
    n = len(y)

    # Moving average
    ma_window = cfg["ma_window"]
    ma = pd.Series(y).rolling(window=ma_window, center=True).mean()

    # Train/test split: first 80% train, last 20% test (chronological)
    split_idx = int(n * 0.8)
    y_train = y[:split_idx]
    y_test = y[split_idx:]

    # Time index (1-based)
    t_all = np.arange(1, n + 1, dtype=float)
    t_train = t_all[:split_idx]
    t_test = t_all[split_idx:]

    all_models = []
    for order in [1, 2, 3]:
        # Construct polynomial features
        X_train = np.column_stack([t_train ** p for p in range(1, order + 1)])
        X_test = np.column_stack([t_test ** p for p in range(1, order + 1)])

        model = LinearRegression()
        model.fit(X_train, y_train)

        pred_train = model.predict(X_train)
        pred_test = model.predict(X_test)

        train_rmse = float(np.sqrt(mean_squared_error(y_train, pred_train)))
        test_rmse = float(np.sqrt(mean_squared_error(y_test, pred_test)))
        test_r2 = float(r2_score(y_test, pred_test))

        all_models.append({
            "order": order,
            "train_rmse": round(train_rmse, 4),
            "test_rmse": round(test_rmse, 4),
            "test_r2": round(test_r2, 6),
            "model": model,
        })

    # Select best model by lowest test RMSE
    best = min(all_models, key=lambda m: m["test_rmse"])
    best_order = best["order"]
    best_model = best["model"]

    # Generate 30-step-ahead forecast
    t_forecast = np.arange(n + 1, n + 31, dtype=float)
    X_forecast = np.column_stack([t_forecast ** p for p in range(1, best_order + 1)])
    forecast_30 = best_model.predict(X_forecast).tolist()

    # Check for overfitting
    order3 = [m for m in all_models if m["order"] == 3][0]
    overfitting_detected = any(
        order3["test_rmse"] >= m["test_rmse"]
        for m in all_models if m["order"] < 3
    )

    # Store results (without sklearn model objects)
    results[series_name] = {
        "best_order": best_order,
        "train_rmse": best["train_rmse"],
        "test_rmse": best["test_rmse"],
        "test_r2": best["test_r2"],
        "all_models": [
            {
                "order": m["order"],
                "train_rmse": m["train_rmse"],
                "test_rmse": m["test_rmse"],
                "test_r2": m["test_r2"],
            }
            for m in all_models
        ],
        "forecast_30": [round(v, 2) for v in forecast_30],
        "moving_average_window": ma_window,
    }

    # Report section
    order_names = {1: "linear", 2: "quadratic", 3: "cubic"}
    report_lines.append("-" * 70)
    report_lines.append(f"Series: {series_name}")
    report_lines.append("-" * 70)
    report_lines.append(f"Number of observations: {n}")
    report_lines.append(f"Moving average window: {ma_window}")
    report_lines.append(f"Train/test split: {split_idx}/{n - split_idx}")
    report_lines.append("")
    report_lines.append("Model comparison:")
    for m in all_models:
        report_lines.append(
            f"  Order {m['order']} ({order_names[m['order']]}): "
            f"Train RMSE={m['train_rmse']:.4f}, "
            f"Test RMSE={m['test_rmse']:.4f}, "
            f"Test R²={m['test_r2']:.6f}"
        )
    report_lines.append("")
    report_lines.append(
        f"Best model: Order {best_order} ({order_names[best_order]}) "
        f"with test RMSE={best['test_rmse']:.4f}"
    )
    report_lines.append("")

    # Describe trend pattern
    if best_order == 1:
        report_lines.append(
            f"Observed trend pattern: The {series_name} series exhibits a predominantly "
            f"linear trend. A straight-line fit captures the main direction of the data "
            f"over time without unnecessary complexity."
        )
    elif best_order == 2:
        report_lines.append(
            f"Observed trend pattern: The {series_name} series shows a quadratic (curved) "
            f"trend. The rate of change is itself changing over time, requiring a "
            f"second-degree polynomial to adequately capture the curvature."
        )
    else:
        report_lines.append(
            f"Observed trend pattern: The {series_name} series requires a cubic polynomial "
            f"to capture its trend, suggesting inflection points in the long-run behavior."
        )

    report_lines.append("")

    if overfitting_detected:
        report_lines.append(
            f"WARNING: Overfitting detected for {series_name}. The cubic (order=3) model "
            f"has a test RMSE of {order3['test_rmse']:.4f}, which is worse than at least "
            f"one lower-order model. This indicates the higher-order polynomial is fitting "
            f"noise in the training data rather than the true underlying trend."
        )
    else:
        report_lines.append(
            f"No clear overfitting detected for {series_name} — all models show improving "
            f"or comparable test performance with increasing order."
        )
    report_lines.append("")

# Comparison section
report_lines.append("=" * 70)
report_lines.append("CROSS-SERIES COMPARISON")
report_lines.append("=" * 70)
report_lines.append("")

r2_values = {name: results[name]["test_r2"] for name in results}
strongest = max(r2_values, key=r2_values.get)
weakest = min(r2_values, key=r2_values.get)

report_lines.append(
    f"Strongest trend: {strongest} (test R²={r2_values[strongest]:.4f}). "
    f"The trend model explains the most variance in this series."
)
report_lines.append(
    f"Weakest trend: {weakest} (test R²={r2_values[weakest]:.4f}). "
    f"This series has the most residual variance unexplained by the trend."
)
report_lines.append("")
report_lines.append(
    "Overall findings: Polynomial trend models of varying orders were fitted to three "
    "diverse time series. The analysis demonstrates that choosing the right polynomial "
    "order is critical — overfitting with higher-order polynomials can degrade "
    "out-of-sample performance. A chronological train/test split ensures realistic "
    "evaluation of forecast quality."
)
report_lines.append("")

# Write outputs
with open("/results/trend_analysis.json", "w") as f:
    json.dump(results, f, indent=2)

with open("/results/report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("Done. Results written to /results/trend_analysis.json and /results/report.txt")
PYEOF
