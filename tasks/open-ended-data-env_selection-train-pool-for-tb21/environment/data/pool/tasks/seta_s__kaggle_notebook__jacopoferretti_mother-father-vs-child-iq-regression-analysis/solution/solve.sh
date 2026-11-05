#!/bin/bash

cat > /home/user/workspace/analysis.py << 'PYEOF'
import json
import math
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import statsmodels.api as sm

SEED = 42
np.random.seed(SEED)

# ========== 1. kid_iq analysis ==========
kid_iq = pd.read_csv("/home/user/datasets/kid_iq.csv")
# Drop unnamed index column
if kid_iq.columns[0] == "" or kid_iq.columns[0].startswith("Unnamed"):
    kid_iq = kid_iq.iloc[:, 1:]

features = ["mom_hs", "mom_iq", "mom_work", "mom_age"]
target = "kid_score"

# Outlier detection using IQR on mom_iq
Q1 = kid_iq["mom_iq"].quantile(0.25)
Q3 = kid_iq["mom_iq"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outlier_mask = (kid_iq["mom_iq"] < lower) | (kid_iq["mom_iq"] > upper)
outliers_found = int(outlier_mask.sum())

# Cap outliers rather than remove (preserve data)
kid_iq_clean = kid_iq.copy()
kid_iq_clean.loc[kid_iq_clean["mom_iq"] < lower, "mom_iq"] = lower
kid_iq_clean.loc[kid_iq_clean["mom_iq"] > upper, "mom_iq"] = upper

X = kid_iq_clean[features].values
y = kid_iq_clean[target].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=SEED)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "LinearRegression": LinearRegression(),
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=SEED),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=SEED),
}

results = []
best_rmse = float("inf")
best_name = ""
best_model = None

for name, model in models.items():
    if name in ["RandomForest", "GradientBoosting"]:
        model.fit(X_train_scaled, y_train)
        train_pred = model.predict(X_train_scaled)
        test_pred = model.predict(X_test_scaled)
    else:
        model.fit(X_train_scaled, y_train)
        train_pred = model.predict(X_train_scaled)
        test_pred = model.predict(X_test_scaled)

    train_rmse = math.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = math.sqrt(mean_squared_error(y_test, test_pred))
    train_mae = mean_absolute_error(y_train, train_pred)
    test_mae = mean_absolute_error(y_test, test_pred)

    results.append({
        "name": name,
        "train_rmse": round(train_rmse, 4),
        "test_rmse": round(test_rmse, 4),
        "train_mae": round(train_mae, 4),
        "test_mae": round(test_mae, 4),
    })

    if test_rmse < best_rmse:
        best_rmse = test_rmse
        best_name = name
        best_model = model
        best_test_pred = test_pred

# Feature importance from RandomForest
rf_model = models["RandomForest"]
importances = rf_model.feature_importances_
feature_importance = {features[i]: round(float(importances[i]), 4) for i in range(len(features))}

# Cross-validation on best model
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5, scoring="neg_mean_squared_error")
cv_rmse = [round(math.sqrt(-s), 4) for s in cv_scores]

# Save predictions
pred_df = pd.DataFrame({"actual": y_test, "predicted": best_test_pred})
pred_df.to_csv("/home/user/workspace/predictions.csv", index=False)

# ========== 2. gifted clustering ==========
gifted = pd.read_csv("/home/user/datasets/gifted.csv")
gifted_features = gifted.drop(columns=["score"]).values

gifted_scaler = StandardScaler()
gifted_scaled = gifted_scaler.fit_transform(gifted_features)

pca = PCA(random_state=SEED)
pca_result = pca.fit_transform(gifted_scaled)
variance_explained = [round(float(v), 4) for v in pca.explained_variance_ratio_]

# Use first 5 components
n_components = 5
pca5 = PCA(n_components=n_components, random_state=SEED)
pca5_result = pca5.fit_transform(gifted_scaled)
pca5_variance = [round(float(v), 4) for v in pca5.explained_variance_ratio_]

# Determine optimal clusters
best_sil = -1
best_k = 2
for k in range(2, 6):
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    labels = km.fit_predict(pca5_result)
    sil = silhouette_score(pca5_result, labels)
    if sil > best_sil:
        best_sil = sil
        best_k = k

km_final = KMeans(n_clusters=best_k, random_state=SEED, n_init=10)
cluster_labels = km_final.fit_predict(pca5_result)
final_sil = silhouette_score(pca5_result, cluster_labels)

# Cluster means
gifted_with_cluster = gifted.copy()
gifted_with_cluster["cluster"] = cluster_labels
cluster_means = {}
for c in range(best_k):
    cluster_data = gifted_with_cluster[gifted_with_cluster["cluster"] == c].drop(columns=["cluster"])
    cluster_means[f"cluster_{c}"] = {col: round(float(cluster_data[col].mean()), 2) for col in cluster_data.columns}

# ========== 3. child_iq regression ==========
child_iq = pd.read_csv("/home/user/datasets/child_iq.csv")
if child_iq.columns[0] == "" or child_iq.columns[0].startswith("Unnamed"):
    child_iq = child_iq.iloc[:, 1:]

# Treat educ_cat as categorical
child_iq["educ_cat"] = child_iq["educ_cat"].astype("category")
dummies = pd.get_dummies(child_iq["educ_cat"], prefix="educ", drop_first=True)
X_child = pd.concat([child_iq[["momage"]], dummies], axis=1).astype(float)
X_child = sm.add_constant(X_child)
y_child = child_iq["ppvt"].astype(float)

ols_model = sm.OLS(y_child, X_child).fit()
child_r2 = round(float(ols_model.rsquared), 4)
sig_predictors = [name for name, pval in ols_model.pvalues.items() if pval < 0.05 and name != "const"]

# ========== 4. twins analysis ==========
twins = pd.read_csv("/home/user/datasets/twins.csv")
# Clean column names
twins.columns = [c.strip().strip('"') for c in twins.columns]

foster_col = [c for c in twins.columns if "foster" in c.lower()][0]
bio_col = [c for c in twins.columns if "bio" in c.lower()][0]

correlation = round(float(twins[foster_col].corr(twins[bio_col])), 4)

# OLS: Biological ~ Foster
X_twins = sm.add_constant(twins[foster_col].astype(float))
y_twins = twins[bio_col].astype(float)
twins_ols = sm.OLS(y_twins, X_twins).fit()
twins_r2 = round(float(twins_ols.rsquared), 4)

# ========== 5. Compile report ==========
report = {
    "kid_iq_analysis": {
        "models_compared": results,
        "best_model": best_name,
        "feature_importance": feature_importance,
        "cv_scores": cv_rmse,
    },
    "gifted_clustering": {
        "n_clusters": best_k,
        "silhouette_score": round(float(final_sil), 4),
        "cluster_means": cluster_means,
        "pca_variance_explained": pca5_variance,
    },
    "child_iq_regression": {
        "ols_r_squared": child_r2,
        "significant_predictors": sig_predictors,
    },
    "twins_analysis": {
        "correlation": correlation,
        "ols_r_squared": twins_r2,
    },
    "preprocessing": {
        "outlier_method": "IQR (Interquartile Range)",
        "scaling_method": "StandardScaler",
        "outliers_found": outliers_found,
        "reasoning": "Used IQR method for outlier detection on mom_iq as it is robust to non-normal distributions. Outliers were capped (winsorized) rather than removed to preserve sample size. StandardScaler was chosen for feature scaling to normalize features to zero mean and unit variance, which is important for distance-based algorithms and regularized models. Train/test split was performed before scaling to prevent data leakage from the test set into the training preprocessing.",
    },
}

with open("/home/user/workspace/report.json", "w") as f:
    json.dump(report, f, indent=2)

print("Analysis complete. Files written to /home/user/workspace/")
PYEOF

cd /home/user/workspace && python analysis.py
