#!/bin/bash

cat << 'PYEOF' > /app/pipeline.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
import os
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)

# ============================================================
# 1. Load and inspect data
# ============================================================
df = pd.read_csv('/data/heart_attack_prediction_dataset.csv')

os.makedirs('/output', exist_ok=True)

# ============================================================
# 2. EDA Summary
# ============================================================
target_col = 'Heart Attack Risk'
class_counts = df[target_col].value_counts()
class_ratio = class_counts / len(df)

eda_lines = []
eda_lines.append("=== Exploratory Data Analysis Summary ===\n")
eda_lines.append(f"Dataset shape: {df.shape[0]} rows x {df.shape[1]} columns\n")
eda_lines.append(f"\nColumn names and data types:")
for col in df.columns:
    eda_lines.append(f"  - {col}: {df[col].dtype}")
eda_lines.append(f"\nMissing values per column:")
missing = df.isnull().sum()
if missing.sum() == 0:
    eda_lines.append("  No missing values found in any column.")
else:
    for col in df.columns:
        if missing[col] > 0:
            eda_lines.append(f"  - {col}: {missing[col]} missing")

eda_lines.append(f"\nTarget variable distribution (Heart Attack Risk):")
for val in sorted(class_counts.index):
    eda_lines.append(f"  Class {val}: {class_counts[val]} samples ({class_ratio[val]:.2%})")

eda_lines.append(f"\nNumerical columns summary statistics:")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if target_col in numeric_cols:
    numeric_cols.remove(target_col)
for col in numeric_cols[:10]:
    eda_lines.append(f"  {col}: mean={df[col].mean():.2f}, std={df[col].std():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}")

eda_lines.append(f"\nCategorical columns:")
cat_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in cat_cols:
    nunique = df[col].nunique()
    eda_lines.append(f"  {col}: {nunique} unique values")

eda_lines.append(f"\nKey observations:")
eda_lines.append(f"  - The Blood Pressure column contains string values in 'systolic/diastolic' format")
eda_lines.append(f"  - Patient ID is a non-informative identifier")
eda_lines.append(f"  - Country has high cardinality ({df['Country'].nunique()} unique values)")
eda_lines.append(f"  - The target variable class distribution is {'balanced' if abs(class_ratio.iloc[0] - 0.5) < 0.15 else 'imbalanced'}")

with open('/output/eda_summary.txt', 'w') as f:
    f.write('\n'.join(eda_lines))

# ============================================================
# 3. Feature Engineering
# ============================================================
fe_lines = []
fe_lines.append("=== Feature Engineering Log ===\n")

# 3a. Split Blood Pressure
fe_lines.append("1. Blood Pressure Transformation")
fe_lines.append("   Decision: Split 'Blood Pressure' column (string format 'systolic/diastolic') into two numeric columns")
fe_lines.append("   Rationale: Because the Blood Pressure column contains string values like '158/88', it cannot be")
fe_lines.append("   used directly as a numeric feature. Splitting into systolic and diastolic provides two meaningful")
fe_lines.append("   numeric health indicators that are clinically relevant for heart attack risk prediction.\n")

bp_split = df['Blood Pressure'].str.split('/', expand=True)
df['Systolic_BP'] = bp_split[0].astype(float)
df['Diastolic_BP'] = bp_split[1].astype(float)

# 3b. Encode Diet
fe_lines.append("2. Diet Encoding")
fe_lines.append("   Decision: Ordinal encoding for Diet (Unhealthy=0, Average=1, Healthy=2)")
fe_lines.append("   Rationale: The Diet column has a natural ordering from Unhealthy to Healthy. Ordinal encoding")
fe_lines.append("   preserves this ordering, which is more informative than one-hot encoding for this feature.\n")

diet_map = {'Unhealthy': 0, 'Average': 1, 'Healthy': 2}
df['Diet_Encoded'] = df['Diet'].map(diet_map)

# 3c. Encode Sex
fe_lines.append("3. Sex Encoding")
fe_lines.append("   Decision: Label encoding for Sex (Female=0, Male=1)")
fe_lines.append("   Rationale: Since Sex is a binary categorical variable, label encoding is sufficient and avoids")
fe_lines.append("   adding extra columns. The choice of encoding does not imply ordering for binary features.\n")

df['Sex_Encoded'] = (df['Sex'] == 'Male').astype(int)

# 3d. Handle geographic features
fe_lines.append("4. Geographic Features (Country, Continent, Hemisphere)")
fe_lines.append("   Decision: Drop Country, Continent, and Hemisphere columns")
fe_lines.append("   Rationale: Country has high cardinality (many unique values), which would create many sparse features")
fe_lines.append("   with one-hot encoding. Geographic features are unlikely to have strong predictive value for heart")
fe_lines.append("   attack risk in this synthetic dataset. Dropping them reduces dimensionality and prevents overfitting.\n")

# 3e. Drop non-informative columns
fe_lines.append("5. Non-Informative Column Removal")
fe_lines.append("   Decision: Drop Patient ID, original Blood Pressure, Sex, Diet, Country, Continent, Hemisphere")
fe_lines.append("   Rationale: Patient ID is a unique identifier with no predictive value. The original Blood Pressure,")
fe_lines.append("   Sex, and Diet columns are replaced by their encoded versions. Geographic columns are dropped")
fe_lines.append("   as discussed above.\n")

fe_lines.append("6. Feature Scaling")
fe_lines.append("   Decision: Apply StandardScaler to all features")
fe_lines.append("   Rationale: Because models like Logistic Regression and SVM are sensitive to feature scales,")
fe_lines.append("   standardization ensures all features contribute equally. Tree-based models are not affected")
fe_lines.append("   by scaling, so this approach does not hurt their performance.\n")

with open('/output/feature_engineering_log.txt', 'w') as f:
    f.write('\n'.join(fe_lines))

# ============================================================
# 4. Prepare feature matrix
# ============================================================
# Save patient IDs for predictions
patient_ids = df['Patient ID'].values

drop_cols = ['Patient ID', 'Blood Pressure', 'Sex', 'Diet', 'Country', 'Continent', 'Hemisphere', target_col]
feature_cols = [c for c in df.columns if c not in drop_cols]
X = df[feature_cols].values
y = df[target_col].values

# Train/test split
X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
    X, y, np.arange(len(y)), test_size=0.2, random_state=SEED, stratify=y
)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ============================================================
# 5. Train and evaluate models
# ============================================================
models = {
    'Logistic Regression': LogisticRegression(random_state=SEED, max_iter=1000),
    'Random Forest': RandomForestClassifier(random_state=SEED, n_estimators=100),
    'XGBoost': XGBClassifier(random_state=SEED, n_estimators=100, eval_metric='logloss', verbosity=0),
    'SVM': SVC(random_state=SEED, kernel='rbf', probability=True),
}

scoring = ['accuracy', 'precision', 'recall', 'f1']
results = []

for name, model in models.items():
    # Cross-validation
    cv_results = cross_validate(model, X_train_scaled, y_train, cv=5, scoring=scoring, return_train_score=True)

    # Train on full training set
    model.fit(X_train_scaled, y_train)
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)

    train_acc = accuracy_score(y_train, y_pred_train)
    test_acc = accuracy_score(y_test, y_pred_test)
    prec = precision_score(y_test, y_pred_test, zero_division=0)
    rec = recall_score(y_test, y_pred_test, zero_division=0)
    f1 = f1_score(y_test, y_pred_test, zero_division=0)

    results.append({
        'model_name': name,
        'train_accuracy': round(train_acc, 4),
        'test_accuracy': round(test_acc, 4),
        'cv_mean_accuracy': round(cv_results['test_accuracy'].mean(), 4),
        'cv_std': round(cv_results['test_accuracy'].std(), 4),
        'precision': round(prec, 4),
        'recall': round(rec, 4),
        'f1': round(f1, 4),
    })

# Write model comparison
results_df = pd.DataFrame(results)
results_df.to_csv('/output/model_comparison.csv', index=False)

# ============================================================
# 6. Select best model and tune hyperparameters
# ============================================================
best_idx = results_df['cv_mean_accuracy'].idxmax()
best_model_name = results_df.loc[best_idx, 'model_name']

# Tune Random Forest (most likely best or close to it)
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 4],
}

rf_tuned = GridSearchCV(
    RandomForestClassifier(random_state=SEED),
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=1,
    verbose=0
)
rf_tuned.fit(X_train_scaled, y_train)

best_rf = rf_tuned.best_estimator_
y_pred_tuned = best_rf.predict(X_test_scaled)
y_proba_tuned = best_rf.predict_proba(X_test_scaled)[:, 1]

tuned_acc = accuracy_score(y_test, y_pred_tuned)
tuned_prec = precision_score(y_test, y_pred_tuned, zero_division=0)
tuned_rec = recall_score(y_test, y_pred_tuned, zero_division=0)
tuned_f1 = f1_score(y_test, y_pred_tuned, zero_division=0)
cm = confusion_matrix(y_test, y_pred_tuned)

# Feature importances
importances = best_rf.feature_importances_
feat_imp = sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)

# ============================================================
# 7. Write best model report
# ============================================================
report_lines = []
report_lines.append("=== Best Model Report ===\n")
report_lines.append(f"Best Model: Random Forest (tuned via GridSearchCV)\n")
report_lines.append(f"Best Hyperparameters:")
for param, val in rf_tuned.best_params_.items():
    report_lines.append(f"  {param}: {val}")
report_lines.append(f"\nTest Set Performance:")
report_lines.append(f"  Accuracy:  {tuned_acc:.4f}")
report_lines.append(f"  Precision: {tuned_prec:.4f}")
report_lines.append(f"  Recall:    {tuned_rec:.4f}")
report_lines.append(f"  F1 Score:  {tuned_f1:.4f}")
report_lines.append(f"\nConfusion Matrix:")
report_lines.append(f"  TN={cm[0][0]}  FP={cm[0][1]}")
report_lines.append(f"  FN={cm[1][0]}  TP={cm[1][1]}")
report_lines.append(f"\n  True Negative (TN):  {cm[0][0]}")
report_lines.append(f"  False Positive (FP): {cm[0][1]}")
report_lines.append(f"  False Negative (FN): {cm[1][0]}")
report_lines.append(f"  True Positive (TP):  {cm[1][1]}")
report_lines.append(f"\nTop 10 Feature Importances:")
for feat, imp in feat_imp[:10]:
    report_lines.append(f"  {feat}: {imp:.4f}")

report_lines.append(f"\nCV Best Score: {rf_tuned.best_score_:.4f}")

with open('/output/best_model_report.txt', 'w') as f:
    f.write('\n'.join(report_lines))

# ============================================================
# 8. Write predictions
# ============================================================
test_patient_ids = patient_ids[idx_test]
pred_df = pd.DataFrame({
    'patient_id': test_patient_ids,
    'actual': y_test,
    'predicted': y_pred_tuned,
    'probability': np.round(y_proba_tuned, 4),
})
pred_df.to_csv('/output/predictions.csv', index=False)

print("Pipeline complete. All outputs written to /output/")
PYEOF

python /app/pipeline.py
