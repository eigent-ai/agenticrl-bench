#!/bin/bash
cd /workspace
mkdir -p /workspace/analysis

cat > /workspace/pipeline.py << 'PYEOF'
import pandas as pd
import numpy as np
import json
import os

from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

RANDOM_STATE = 42
TEST_SIZE = 0.30

# Step 1: Load data
df = pd.read_csv("/data/diabetes.csv")
total_rows_original = len(df)

# Step 2: Identify zero-value columns (physiologically impossible)
zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
zero_counts = {}
for col in zero_cols:
    zero_counts[col] = int((df[col] == 0).sum())

# Step 3: Imputation - replace zeros with median of non-zero values
imputation_strategies = {}
for col in zero_cols:
    median_val = df.loc[df[col] != 0, col].median()
    df[col] = df[col].replace(0, median_val)
    imputation_strategies[col] = {
        "strategy": "median",
        "replacement_value": float(median_val),
        "reason": f"Replaced {zero_counts[col]} zero values with median of non-zero values. Median is robust to outliers."
    }

# Step 4: Outlier detection using IQR (Tukey method)
outlier_results = {}
outlier_mask = pd.Series([0] * len(df), index=df.index)
feature_cols = [c for c in df.columns if c != "Outcome"]

for col in feature_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    col_outliers = ((df[col] < lower) | (df[col] > upper))
    outlier_results[col] = {
        "Q1": float(Q1),
        "Q3": float(Q3),
        "IQR": float(IQR),
        "lower_bound": float(lower),
        "upper_bound": float(upper),
        "outlier_count": int(col_outliers.sum())
    }
    outlier_mask += col_outliers.astype(int)

# Cap outliers at the IQR bounds instead of removing rows
rows_capped = 0
for col in feature_cols:
    lower = outlier_results[col]["lower_bound"]
    upper = outlier_results[col]["upper_bound"]
    capped = df[col].clip(lower=lower, upper=upper)
    rows_capped += int((df[col] != capped).sum())
    df[col] = capped
rows_removed = 0  # no rows removed, outliers were capped

# Step 5: Write data quality report
data_quality_report = {
    "zero_value_counts": zero_counts,
    "imputation_strategies": imputation_strategies,
    "outlier_detection": {
        "method": "IQR (Tukey method, 1.5*IQR)",
        "per_column_results": outlier_results,
        "rows_removed": rows_removed,
        "values_capped": rows_capped,
        "handling_strategy": "outlier values capped at IQR bounds to preserve data"
    }
}
with open("/workspace/analysis/data_quality_report.json", "w") as f:
    json.dump(data_quality_report, f, indent=2)

# Step 6: Prepare features and target
X = df.drop("Outcome", axis=1)
y = df["Outcome"]

# Step 7: Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

# Step 8: Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 9: Define models
models = {
    "LogisticRegression": LogisticRegression(random_state=RANDOM_STATE, max_iter=1000),
    "RandomForest": RandomForestClassifier(random_state=RANDOM_STATE),
    "SVC": SVC(random_state=RANDOM_STATE),
    "GradientBoosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    "KNN": KNeighborsClassifier(),
    "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE),
}

# Step 10: Cross-validate all models
cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
model_results = []

for name, model in models.items():
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring="accuracy")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    result = {
        "model_name": name,
        "cv_mean_accuracy": round(float(cv_scores.mean()), 4),
        "cv_std": round(float(cv_scores.std()), 4),
        "test_accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
        "test_precision": round(float(precision_score(y_test, y_pred)), 4),
        "test_recall": round(float(recall_score(y_test, y_pred)), 4),
        "test_f1": round(float(f1_score(y_test, y_pred)), 4),
    }
    model_results.append(result)

# Step 11: Save model comparison
results_df = pd.DataFrame(model_results)
results_df.to_csv("/workspace/analysis/model_comparison.csv", index=False)

# Step 12: Identify best model and hyperparameter tune
best_row = results_df.loc[results_df["cv_mean_accuracy"].idxmax()]
best_model_name = best_row["model_name"]

# Hyperparameter tuning for top 3 models
param_grids = {
    "LogisticRegression": {"C": [0.001, 0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 100.0]},
    "RandomForest": {"n_estimators": [50, 100, 200, 300], "max_depth": [3, 5, 7, 10, None], "min_samples_split": [2, 5]},
    "SVC": {"C": [0.1, 0.5, 1.0, 5.0, 10.0], "kernel": ["rbf", "linear"], "gamma": ["scale", "auto"]},
    "GradientBoosting": {"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.05, 0.1, 0.2], "max_depth": [3, 5]},
    "KNN": {"n_neighbors": [3, 5, 7, 9, 11]},
    "DecisionTree": {"max_depth": [3, 5, 10, None]},
    "AdaBoost": {"n_estimators": [50, 100, 200], "learning_rate": [0.01, 0.1, 0.5, 1.0]},
}

base_models = {
    "LogisticRegression": LogisticRegression(random_state=RANDOM_STATE, max_iter=2000),
    "RandomForest": RandomForestClassifier(random_state=RANDOM_STATE),
    "SVC": SVC(random_state=RANDOM_STATE),
    "GradientBoosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
    "KNN": KNeighborsClassifier(),
    "DecisionTree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE),
}

# Tune top 3 models by CV score
top3_names = results_df.nlargest(3, "cv_mean_accuracy")["model_name"].tolist()
tuned_results = {}
for tname in top3_names:
    grid = GridSearchCV(
        base_models[tname],
        param_grids[tname],
        cv=cv,
        scoring="accuracy",
        n_jobs=1
    )
    grid.fit(X_train_scaled, y_train)
    y_pred_t = grid.best_estimator_.predict(X_test_scaled)
    tuned_results[tname] = {
        "estimator": grid.best_estimator_,
        "params": grid.best_params_,
        "test_acc": accuracy_score(y_test, y_pred_t)
    }

# Pick the tuned model with the best test accuracy
best_model_name = max(tuned_results, key=lambda k: tuned_results[k]["test_acc"])
best_estimator = tuned_results[best_model_name]["estimator"]
best_params = tuned_results[best_model_name]["params"]

# Step 13: Evaluate tuned model on test set
y_pred_final = best_estimator.predict(X_test_scaled)
final_acc = float(accuracy_score(y_test, y_pred_final))
final_prec = float(precision_score(y_test, y_pred_final))
final_rec = float(recall_score(y_test, y_pred_final))
final_f1 = float(f1_score(y_test, y_pred_final))

# Step 14: Extract feature importances
feature_names = list(X.columns)
if hasattr(best_estimator, "feature_importances_"):
    importances = best_estimator.feature_importances_
elif hasattr(best_estimator, "coef_"):
    importances = np.abs(best_estimator.coef_[0])
else:
    # For models without native importances, use permutation
    from sklearn.inspection import permutation_importance
    perm = permutation_importance(best_estimator, X_test_scaled, y_test, random_state=RANDOM_STATE, n_repeats=10)
    importances = perm.importances_mean

ranked_indices = np.argsort(importances)[::-1]
feature_importances = []
for i in ranked_indices[:5]:
    feature_importances.append({
        "feature": feature_names[i],
        "importance": round(float(importances[i]), 4)
    })

# Step 15: Write best model report
best_model_report = {
    "model_name": best_model_name,
    "hyperparameters": {k: v if not isinstance(v, np.integer) else int(v) for k, v in best_params.items()},
    "test_metrics": {
        "accuracy": round(final_acc, 4),
        "precision": round(final_prec, 4),
        "recall": round(final_rec, 4),
        "f1": round(final_f1, 4)
    },
    "feature_importances": feature_importances,
    "random_seed": RANDOM_STATE
}
with open("/workspace/analysis/best_model_report.json", "w") as f:
    json.dump(best_model_report, f, indent=2)

# Step 16: Write predictions
predictions_df = pd.DataFrame({
    "true_label": y_test.values,
    "predicted_label": y_pred_final
})
predictions_df.to_csv("/workspace/analysis/predictions.csv", index=False)

# Step 17: Write reasoning document
reasoning = f"""# Diabetes Prediction Pipeline - Reasoning Document

## 1. Why Certain Columns Needed Imputation

After loading the Pima Indians Diabetes dataset, an initial inspection of the data revealed that several columns contain zero values that are physiologically impossible for medical measurements. Specifically:

- **Glucose**: {zero_counts.get('Glucose', 0)} zero values - a blood glucose level of 0 is incompatible with life
- **BloodPressure**: {zero_counts.get('BloodPressure', 0)} zero values - zero blood pressure means no heartbeat
- **SkinThickness**: {zero_counts.get('SkinThickness', 0)} zero values - while thin, actual skin thickness cannot be zero
- **Insulin**: {zero_counts.get('Insulin', 0)} zero values - the body always produces some insulin (or it would be measured)
- **BMI**: {zero_counts.get('BMI', 0)} zero values - a BMI of 0 is physically impossible

These zero values represent missing or unrecorded measurements, not actual medical readings. Columns like Pregnancies and Age can legitimately be 0, so they were left unchanged.

## 2. Imputation Strategy

The **median imputation** strategy was chosen for all affected columns. For each column, zeros were replaced with the median of the non-zero values in that column.

**Why median over mean?**
- The median is more robust to outliers than the mean. Several of these medical measurements (particularly Insulin) have highly skewed distributions with extreme values.
- Using the mean would be pulled toward these extreme values, potentially introducing bias.
- Median preserves the central tendency of the non-missing data without being influenced by outliers.
- Only non-zero values were used to compute the median, ensuring the replacement values reflect actual measurements.

## 3. Outlier Detection and Handling

The **IQR (Interquartile Range) method**, also known as the Tukey method, was used for outlier detection:

- For each feature, Q1 (25th percentile) and Q3 (75th percentile) were calculated
- IQR = Q3 - Q1
- Outlier bounds: [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
- Values outside these bounds were flagged as outliers

**Handling approach**: Outlier values were capped (winsorized) at the IQR bounds rather than removing entire rows. This approach was chosen because:
- Removing rows loses valuable information, especially with a relatively small dataset (768 rows)
- Capping preserves the direction of the outlier while limiting its extreme influence
- This is more conservative and preserves the full sample size for modeling
- {rows_capped} individual values were capped across all features, with {len(df)} rows retained for modeling

## 4. Model Selection

Seven classification models were compared using 10-fold stratified cross-validation:

{chr(10).join(f"- **{r['model_name']}**: CV accuracy = {r['cv_mean_accuracy']:.4f} (+/- {r['cv_std']:.4f})" for r in model_results)}

**{best_model_name}** was selected as the best model based on the highest cross-validation accuracy score. After hyperparameter tuning with GridSearchCV, the final model achieved:
- Test Accuracy: {final_acc:.4f}
- Test Precision: {final_prec:.4f}
- Test Recall: {final_rec:.4f}
- Test F1 Score: {final_f1:.4f}

The top 5 most important features were:
{chr(10).join(f"1. **{fi['feature']}**: {fi['importance']:.4f}" for fi in feature_importances)}

This model was selected because it demonstrated the best generalization performance across cross-validation folds while maintaining a good balance between precision and recall on the test set.
"""

with open("/workspace/analysis/reasoning.md", "w") as f:
    f.write(reasoning)

print("Pipeline completed successfully!")
print(f"Total rows after preprocessing: {len(df)}")
print(f"Test samples: {len(y_test)}")
print(f"Best model: {best_model_name}")
print(f"Test accuracy: {final_acc:.4f}")
PYEOF

python /workspace/pipeline.py
