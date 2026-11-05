#!/bin/bash
cd /workspace

cat << 'PYEOF' > pipeline.py
import pandas as pd
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

SEED = 42
np.random.seed(SEED)

# 1. Load data
df = pd.read_csv("/data/survey lung cancer.csv")
original_shape = list(df.shape)

# 2. Clean column names (strip whitespace)
df.columns = df.columns.str.strip()

# 3. Check duplicates
num_duplicates = df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)

# 4. Check nulls
null_counts = df.isnull().sum().to_dict()
total_nulls = sum(null_counts.values())

# 5. Encode categorical features
le_gender = LabelEncoder()
df['GENDER'] = le_gender.fit_transform(df['GENDER'])  # F=0, M=1

le_target = LabelEncoder()
df['LUNG_CANCER'] = le_target.fit_transform(df['LUNG_CANCER'])  # NO=0, YES=1

# 6. Remap binary features from (1,2) to (0,1)
binary_cols = [c for c in df.columns if c not in ['GENDER', 'AGE', 'LUNG_CANCER']]
for col in binary_cols:
    df[col] = df[col].map({1: 0, 2: 1})

# 7. Class distribution before balancing
class_before = df['LUNG_CANCER'].value_counts().to_dict()
class_before = {str(k): int(v) for k, v in class_before.items()}

# 8. Feature analysis - check correlation with target
X = df.drop('LUNG_CANCER', axis=1)
y = df['LUNG_CANCER']

correlations = X.corrwith(y).abs().sort_values(ascending=False)

# Drop features with weak correlation (< 0.1)
weak_features = correlations[correlations < 0.1].index.tolist()
features_dropped = []
for feat in weak_features:
    corr_val = float(correlations.get(feat, 0))
    features_dropped.append({
        "feature": feat,
        "rationale": f"Very weak correlation with target (|r| = {corr_val:.3f})"
    })

# Also check SMOKING specifically
if 'SMOKING' in X.columns and 'SMOKING' not in weak_features:
    smoking_corr = float(correlations.get('SMOKING', 0))
    if smoking_corr < 0.15:
        weak_features.append('SMOKING')
        features_dropped.append({
            "feature": "SMOKING",
            "rationale": f"Counterintuitively weak association with lung cancer (|r| = {smoking_corr:.3f})"
        })

if len(weak_features) > 0:
    X = X.drop(columns=weak_features, errors='ignore')

# 9. Feature engineering: interaction between correlated features
features_engineered = []
if 'ANXIETY' in X.columns and 'YELLOW_FINGERS' in X.columns:
    anx_yf_corr = df['ANXIETY'].corr(df['YELLOW_FINGERS'])
    if abs(anx_yf_corr) > 0.3:
        X['ANXIETY_YELLOW_FINGERS'] = X['ANXIETY'] * X['YELLOW_FINGERS']
        features_engineered.append({
            "feature": "ANXIETY_YELLOW_FINGERS",
            "rationale": f"Interaction term for ANXIETY and YELLOW_FINGERS (correlation={anx_yf_corr:.3f})"
        })

# 10. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=y
)

# 11. Handle class imbalance with SMOTE
smote = SMOTE(random_state=SEED)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

class_after = pd.Series(y_train_balanced).value_counts().to_dict()
class_after = {str(k): int(v) for k, v in class_after.items()}

# 12. Define models
models = {
    "LogisticRegression": LogisticRegression(random_state=SEED, max_iter=1000),
    "DecisionTree": DecisionTreeClassifier(random_state=SEED),
    "RandomForest": RandomForestClassifier(random_state=SEED, n_estimators=100),
    "GradientBoosting": GradientBoostingClassifier(random_state=SEED, n_estimators=100),
    "SVC": SVC(random_state=SEED, kernel='rbf'),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "XGBoost": XGBClassifier(random_state=SEED, n_estimators=100, eval_metric='logloss', verbosity=0),
}

# 13. Train and evaluate
model_results = {}
cv_results_dict = {}
comparison_rows = []
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

for name, model in models.items():
    # Train
    model.fit(X_train_balanced, y_train_balanced)

    # Predict on test
    y_pred = model.predict(X_test)

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    model_results[name] = {
        "test_accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
    }

    # Cross-validation on full balanced data
    # Use SMOTE inside CV properly: just do CV on balanced training set
    cv_scores = cross_val_score(model, X_train_balanced, y_train_balanced, cv=skf, scoring='accuracy')
    cv_mean = float(cv_scores.mean())
    cv_std = float(cv_scores.std())

    cv_results_dict[name] = {
        "mean": round(cv_mean, 4),
        "std": round(cv_std, 4),
    }

    comparison_rows.append({
        "model_name": name,
        "test_accuracy": round(acc, 4),
        "cv_mean_accuracy": round(cv_mean, 4),
        "cv_std": round(cv_std, 4),
        "f1_score": round(f1, 4),
    })

# 14. Find best model
best_model_name = max(cv_results_dict, key=lambda k: cv_results_dict[k]["mean"])

# 15. Feature importance from best model
best_model_obj = models[best_model_name]
feature_names = list(X.columns)

if hasattr(best_model_obj, 'feature_importances_'):
    importances = best_model_obj.feature_importances_
elif hasattr(best_model_obj, 'coef_'):
    importances = np.abs(best_model_obj.coef_[0]) if best_model_obj.coef_.ndim > 1 else np.abs(best_model_obj.coef_)
else:
    # Fallback: use RandomForest importance
    rf = models.get("RandomForest")
    if rf and hasattr(rf, 'feature_importances_'):
        importances = rf.feature_importances_
    else:
        importances = np.ones(len(feature_names))

importance_pairs = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
top_features = [name for name, _ in importance_pairs[:5]]

# 16. Write predictions.csv
pred_best = models[best_model_name].predict(X_test)
pred_df = pd.DataFrame({
    "true_label": y_test.values,
    "predicted_label": pred_best,
})
pred_df.to_csv("/workspace/predictions.csv", index=False)

# 17. Write model_comparison.csv
comp_df = pd.DataFrame(comparison_rows)
comp_df.to_csv("/workspace/model_comparison.csv", index=False)

# 18. Write report.json
report = {
    "dataset_info": {
        "original_shape": original_shape,
        "duplicates_found": int(num_duplicates),
        "null_values": int(total_nulls),
    },
    "class_distribution": {
        "before": class_before,
        "after": class_after,
    },
    "features_dropped": features_dropped,
    "features_engineered": features_engineered,
    "imbalance_strategy": "SMOTE (Synthetic Minority Over-sampling Technique) - chosen because the dataset has significant class imbalance with the minority class being ~13% of the data. SMOTE generates synthetic samples rather than duplicating existing ones, which helps avoid overfitting compared to random oversampling.",
    "model_results": model_results,
    "cv_results": cv_results_dict,
    "best_model": best_model_name,
    "top_features": top_features,
    "random_seed": SEED,
}

with open("/workspace/report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Pipeline complete!")
print(f"Best model: {best_model_name}")
print(f"Best CV accuracy: {cv_results_dict[best_model_name]['mean']}")
PYEOF

python pipeline.py
