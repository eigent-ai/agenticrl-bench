#!/bin/bash

cat > /workspace/pipeline.py << 'PYEOF'
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Lasso, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import os

# 1. Load data
df = pd.read_csv("/data/Housing.csv")
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Missing values:\n{df.isnull().sum().sum()}")

# 2. Outlier detection and removal using IQR on price and area
outlier_report_lines = []
original_rows = len(df)

for col in ["price", "area"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    n_outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    outlier_report_lines.append(f"  - {col}: {n_outliers} outliers detected (IQR method, bounds [{lower:.0f}, {upper:.0f}])")
    df = df[(df[col] >= lower) & (df[col] <= upper)]

rows_removed = original_rows - len(df)
outlier_report_lines.insert(0, f"Rows removed: {rows_removed} (from {original_rows} to {len(df)})")
print(f"After outlier removal: {len(df)} rows")

# 3. Encode categorical variables
binary_cols = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "prefarea"]
for col in binary_cols:
    df[col] = df[col].map({"yes": 1, "no": 0})

df = pd.get_dummies(df, columns=["furnishingstatus"], drop_first=True)
print(f"After encoding, columns: {list(df.columns)}")

# 4. Separate features and target
target = "price"
X = df.drop(columns=[target])
y = df[target]

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# 6. Feature scaling
scaler = MinMaxScaler()
feature_names = X_train.columns.tolist()
X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=feature_names, index=X_train.index)
X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=feature_names, index=X_test.index)

# 7. Train models
models = {
    "Ridge": Ridge(alpha=1.0, random_state=42),
    "Lasso": Lasso(alpha=1000, random_state=42, max_iter=10000),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
}

results = []
trained_models = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    results.append({"model_name": name, "r2_score": round(r2, 6), "rmse": round(rmse, 2), "mae": round(mae, 2)})
    trained_models[name] = (model, y_pred, r2)
    print(f"{name}: R2={r2:.4f}, RMSE={rmse:.0f}, MAE={mae:.0f}")

# 8. Save model comparison
os.makedirs("/workspace/results", exist_ok=True)
results_df = pd.DataFrame(results)
results_df.to_csv("/workspace/results/model_comparison.csv", index=False)

# 9. Identify best model
best_name = max(trained_models, key=lambda k: trained_models[k][2])
best_model, best_pred, best_r2 = trained_models[best_name]
print(f"\nBest model: {best_name} (R2={best_r2:.4f})")

# 10. Cross-validation on best model
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5, scoring="r2")
cv_df = pd.DataFrame({"fold": range(1, 6), "r2_score": cv_scores.round(6)})
cv_df.to_csv("/workspace/results/best_model_cv.csv", index=False)
print(f"CV scores: {cv_scores}")
print(f"CV mean: {cv_scores.mean():.4f}")

# 11. Feature importance
if hasattr(best_model, "feature_importances_"):
    importances = best_model.feature_importances_
elif hasattr(best_model, "coef_"):
    importances = np.abs(best_model.coef_)
else:
    importances = np.zeros(len(feature_names))

fi_df = pd.DataFrame({"feature": feature_names, "importance": importances})
fi_df = fi_df.sort_values("importance", ascending=False).reset_index(drop=True)
fi_df.to_csv("/workspace/results/feature_importance.csv", index=False)
print(f"\nTop features:\n{fi_df.head(5)}")

# 12. Predictions
pred_df = pd.DataFrame({"actual": y_test.values, "predicted": best_pred})
pred_df.to_csv("/workspace/results/predictions.csv", index=False)

# 13. Preprocessing report
report = f"""Preprocessing Report for Housing Price Regression
==================================================

1. Outlier Detection and Handling
---------------------------------
Method: Interquartile Range (IQR) method applied to 'price' and 'area' columns.
For each column, values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR] were removed.
{chr(10).join(outlier_report_lines)}

2. Encoding Strategy
--------------------
Strategy: One-hot encoding with drop_first=True for the multi-level categorical variable 'furnishingstatus' (3 levels: furnished, semi-furnished, unfurnished).
Binary yes/no columns (mainroad, guestroom, basement, hotwaterheating, airconditioning, prefarea) were mapped to 1/0.
Rationale: One-hot encoding preserves the categorical nature without imposing ordinal relationships. drop_first avoids multicollinearity.

3. Feature Scaling
------------------
Applied MinMaxScaler to all features before model training.
Rationale: Scaling ensures regularized models (Ridge, Lasso) treat all features equally regardless of their original scale. Tree-based models are scale-invariant but scaling does not hurt them.

4. Train/Test Split
-------------------
Split: 80% train, 20% test with random_state=42.
Training samples: {len(X_train)}, Test samples: {len(X_test)}.

5. Model Comparison Summary
---------------------------
Best model: {best_name} with R2 = {best_r2:.4f} on the test set.
Cross-validation mean R2: {cv_scores.mean():.4f} (std: {cv_scores.std():.4f}).
"""

with open("/workspace/results/preprocessing_report.txt", "w") as f:
    f.write(report)

print("\nAll results saved to /workspace/results/")
PYEOF

cd /workspace && python pipeline.py
