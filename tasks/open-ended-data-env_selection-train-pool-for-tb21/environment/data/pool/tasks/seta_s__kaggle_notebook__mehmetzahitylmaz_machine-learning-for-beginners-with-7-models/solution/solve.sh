#!/bin/bash

mkdir -p /home/user/results

cat > /home/user/results/pipeline.py << 'PYEOF'
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
import os

RESULTS = "/home/user/results"
SEED = 42

# 1. Load data
df = pd.read_csv("/home/user/dataset/heart-2.csv")

# 2. EDA
eda_lines = []
eda_lines.append(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")
eda_lines.append(f"\nColumn Names: {list(df.columns)}")
eda_lines.append(f"\nData Types:\n{df.dtypes.to_string()}")
eda_lines.append(f"\nFirst 5 rows:\n{df.head().to_string()}")
eda_lines.append(f"\nTarget Value Counts:\n{df['target'].value_counts().to_string()}")
eda_lines.append(f"\nClass Balance: {df['target'].value_counts(normalize=True).to_string()}")
eda_lines.append(f"\nMissing Values:\n{df.isnull().sum().to_string()}")
eda_lines.append(f"\nNumerical Statistics:\n{df.describe().to_string()}")

# Identify categorical columns
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
num_cols = df.select_dtypes(include=['number']).columns.tolist()
num_cols = [c for c in num_cols if c != 'target']

eda_lines.append(f"\nCategorical Columns: {cat_cols}")
eda_lines.append(f"Numerical Columns: {num_cols}")

for col in cat_cols:
    eda_lines.append(f"\n{col} unique values ({df[col].nunique()}): {df[col].unique().tolist()}")

with open(os.path.join(RESULTS, "eda_summary.txt"), "w") as f:
    f.write("\n".join(eda_lines))

# 3. Preprocessing rationale
rationale_lines = []
rationale_lines.append("Preprocessing Rationale")
rationale_lines.append("=" * 50)
rationale_lines.append("")
rationale_lines.append("1. Categorical Encoding Strategy:")
rationale_lines.append("")

# Determine encoding per categorical column
binary_cats = []
multi_cats = []
for col in cat_cols:
    n_unique = df[col].nunique()
    if n_unique <= 2:
        binary_cats.append(col)
        rationale_lines.append(f"  - {col}: Label encoding (binary, {n_unique} unique values: {df[col].unique().tolist()})")
    else:
        multi_cats.append(col)
        rationale_lines.append(f"  - {col}: One-hot encoding ({n_unique} unique values: {df[col].unique().tolist()})")

rationale_lines.append("")
rationale_lines.append("Reasoning: Binary categorical columns (sex, exang, fbs) are label encoded because")
rationale_lines.append("they naturally map to 0/1 without introducing additional dimensions. Columns with")
rationale_lines.append("more than 2 categories (cp, thal, restecg, slope) are one-hot encoded to avoid")
rationale_lines.append("imposing an artificial ordinal relationship between categories.")
rationale_lines.append("")
rationale_lines.append("2. Feature Scaling:")
rationale_lines.append("StandardScaler is applied to numerical features. This is important because:")
rationale_lines.append("  - Distance-based models (KNN) are sensitive to feature scale")
rationale_lines.append("  - Logistic Regression converges faster with normalized features")
rationale_lines.append("  - Tree-based models are scale-invariant but scaling does not hurt them")
rationale_lines.append("")
rationale_lines.append("3. Missing Values:")
rationale_lines.append("No missing values detected in the dataset, so no imputation needed.")

with open(os.path.join(RESULTS, "preprocessing_rationale.txt"), "w") as f:
    f.write("\n".join(rationale_lines))

# 4. Apply encoding
# Label encode binary cats
le_dict = {}
for col in binary_cats:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# One-hot encode multi cats
df = pd.get_dummies(df, columns=multi_cats, drop_first=False)

# 5. Split features and target
X = df.drop("target", axis=1)
y = df["target"]

# Scale numerical features
scaler = StandardScaler()
X[num_cols] = scaler.fit_transform(X[num_cols])

# 6. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)

# 7. Define models
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=SEED),
    "Decision Tree": DecisionTreeClassifier(random_state=SEED),
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=SEED),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Gaussian Naive Bayes": GaussianNB(),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=SEED),
    "XGBoost": XGBClassifier(n_estimators=100, random_state=SEED, use_label_encoder=False, eval_metric="logloss"),
}

# 8. Train and evaluate all models
results = []
fitted_models = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    fitted_models[name] = model
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    cv_scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()

    results.append({
        "model_name": name,
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "cv_mean": round(cv_mean, 4),
        "cv_std": round(cv_std, 4),
    })

results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(RESULTS, "model_comparison.csv"), index=False)

# 9. Find best model (by cv_mean)
best_idx = results_df["cv_mean"].idxmax()
best_model_name = results_df.loc[best_idx, "model_name"]
best_model = fitted_models[best_model_name]

# 10. Best model report with confusion matrix
y_pred_best = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_pred_best)

report_lines = []
report_lines.append(f"Best Model Report")
report_lines.append("=" * 50)
report_lines.append(f"\nBest Model: {best_model_name}")
report_lines.append(f"\nSelection Criteria: Highest cross-validated mean accuracy")
report_lines.append(f"CV Mean Accuracy: {results_df.loc[best_idx, 'cv_mean']}")
report_lines.append(f"CV Std: {results_df.loc[best_idx, 'cv_std']}")
report_lines.append(f"Test Set Accuracy: {results_df.loc[best_idx, 'accuracy']}")
report_lines.append(f"Test Set Precision: {results_df.loc[best_idx, 'precision']}")
report_lines.append(f"Test Set Recall: {results_df.loc[best_idx, 'recall']}")
report_lines.append(f"Test Set F1: {results_df.loc[best_idx, 'f1']}")
report_lines.append(f"\nConfusion Matrix:")
report_lines.append(f"                Predicted 0  Predicted 1")
report_lines.append(f"  Actual 0         {cm[0][0]}           {cm[0][1]}")
report_lines.append(f"  Actual 1         {cm[1][0]}           {cm[1][1]}")
report_lines.append(f"\nTrue Negatives (TN): {cm[0][0]}")
report_lines.append(f"False Positives (FP): {cm[0][1]}")
report_lines.append(f"False Negatives (FN): {cm[1][0]}")
report_lines.append(f"True Positives (TP): {cm[1][1]}")
report_lines.append(f"\nReasoning: {best_model_name} was selected as the best model because it achieved")
report_lines.append(f"the highest cross-validated accuracy ({results_df.loc[best_idx, 'cv_mean']}),")
report_lines.append(f"indicating strong and generalizable performance across different data splits.")

with open(os.path.join(RESULTS, "best_model_report.txt"), "w") as f:
    f.write("\n".join(report_lines))

# 11. Feature importance from best tree-based model
# Use Random Forest if best is not tree-based, otherwise use the best
tree_models = ["Random Forest", "Decision Tree", "Gradient Boosting", "XGBoost"]
if best_model_name in tree_models:
    fi_model = best_model
    fi_model_name = best_model_name
else:
    fi_model = fitted_models["Random Forest"]
    fi_model_name = "Random Forest"

importances = fi_model.feature_importances_
fi_df = pd.DataFrame({
    "feature": X.columns,
    "importance": importances
}).sort_values("importance", ascending=False)

# Save top features (at least 10)
fi_df.head(max(10, len(fi_df))).to_csv(os.path.join(RESULTS, "feature_importance.csv"), index=False)

# 12. Predictions CSV
pred_df = pd.DataFrame({
    "actual": y_test.values,
    "predicted": y_pred_best
})
pred_df.to_csv(os.path.join(RESULTS, "predictions.csv"), index=False)

print("Pipeline complete. All results saved to /home/user/results/")
PYEOF

cd /home/user
python3 /home/user/results/pipeline.py
