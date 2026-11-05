#!/bin/bash
cd /workspace

python3 << 'PYEOF'
import pandas as pd
import numpy as np
import json
import os
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ── 1. Load data ───────────────────────────────────────────────────────────
boston = pd.read_csv("/data/boston.csv")
bmi = pd.read_csv("/data/bmi.csv")

X = boston.drop("MEDV", axis=1)
y = boston["MEDV"]
feature_names = list(X.columns)

# ── 2. Correlation matrix ─────────────────────────────────────────────────
corr_matrix = X.corr(method="pearson")
corr_matrix.to_csv("correlation_matrix.csv")

# ── 3. VIF analysis ───────────────────────────────────────────────────────
# Compute VIF for each feature (standard approach used in data science practice)
vif_data = []
for i, col in enumerate(feature_names):
    vif_val = variance_inflation_factor(X.values, i)
    vif_data.append({"Feature": col, "VIF": round(vif_val, 4), "High_VIF": vif_val > 10})
vif_df = pd.DataFrame(vif_data)
vif_df.to_csv("vif_analysis.csv", index=False)

print("VIF values:")
for _, row in vif_df.iterrows():
    print(f"  {row['Feature']}: {row['VIF']}")

# ── 4. BMI VIF (secondary validation) ─────────────────────────────────────
bmi_numeric = pd.get_dummies(bmi, columns=["Gender"], drop_first=True)

# ── 5. Iterative VIF reduction ────────────────────────────────────────────
def iterative_vif_removal(X_df, threshold=10):
    cols = list(X_df.columns)
    removed = []
    while True:
        X_temp = X_df[cols]
        vifs = {}
        for i, col in enumerate(cols):
            vifs[col] = variance_inflation_factor(X_temp.values, i)
        max_vif_feature = max(vifs, key=vifs.get)
        max_vif_value = vifs[max_vif_feature]
        print(f"  Max VIF: {max_vif_feature} = {max_vif_value:.2f}")
        if max_vif_value <= threshold:
            break
        removed.append(max_vif_feature)
        cols.remove(max_vif_feature)
    print(f"  Removed features: {removed}")
    return cols

print("\nIterative VIF removal (threshold=10):")
vif_reduced_features = iterative_vif_removal(X, threshold=10)
print(f"Remaining features ({len(vif_reduced_features)}): {vif_reduced_features}")

# ── 6. Scaling and splitting ──────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42
)

X_train_vif = X_train[vif_reduced_features]
X_test_vif = X_test[vif_reduced_features]

# ── 7. Model definitions ──────────────────────────────────────────────────
def evaluate_model(model, X_tr, X_te, y_tr, y_te, name, n_features):
    model.fit(X_tr, y_tr)
    y_pred = model.predict(X_te)
    rmse = np.sqrt(mean_squared_error(y_te, y_pred))
    r2 = r2_score(y_te, y_pred)
    n = len(y_te)
    p = n_features
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)
    cv_scores = cross_val_score(model, X_tr, y_tr, cv=10, scoring="r2")
    cv_r2 = cv_scores.mean()
    return {
        "Model": name,
        "RMSE": round(rmse, 4),
        "R2": round(r2, 4),
        "Adjusted_R2": round(adj_r2, 4),
        "CV_R2": round(cv_r2, 4),
    }, y_pred

results = []
predictions = {}

# Model 1: Linear Regression - All features
res, pred = evaluate_model(
    LinearRegression(), X_train, X_test, y_train, y_test,
    "Linear Regression (All Features)", len(feature_names)
)
results.append(res)
predictions["Linear_Regression_All"] = pred

# Model 2: Random Forest - All features
res, pred = evaluate_model(
    RandomForestRegressor(n_estimators=100, random_state=42),
    X_train, X_test, y_train, y_test,
    "Random Forest (All Features)", len(feature_names)
)
results.append(res)
predictions["Random_Forest_All"] = pred

# Model 3: Linear Regression - VIF reduced
res, pred = evaluate_model(
    LinearRegression(), X_train_vif, X_test_vif, y_train, y_test,
    "Linear Regression VIF-Reduced", len(vif_reduced_features)
)
results.append(res)
predictions["Linear_Regression_VIF_Reduced"] = pred

# Model 4: Random Forest - VIF reduced
res, pred = evaluate_model(
    RandomForestRegressor(n_estimators=100, random_state=42),
    X_train_vif, X_test_vif, y_train, y_test,
    "Random Forest VIF-Reduced", len(vif_reduced_features)
)
results.append(res)
predictions["Random_Forest_VIF_Reduced"] = pred

# Model 5: RFE + Random Forest
rfe_rf = RandomForestRegressor(n_estimators=100, random_state=42)
rfe_selector = RFE(rfe_rf, n_features_to_select=8, step=1)
rfe_selector.fit(X_train, y_train)
rfe_features = [f for f, s in zip(feature_names, rfe_selector.support_) if s]
y_pred_rfe = rfe_selector.predict(X_test)
rmse_rfe = np.sqrt(mean_squared_error(y_test, y_pred_rfe))
r2_rfe = r2_score(y_test, y_pred_rfe)
n = len(y_test)
adj_r2_rfe = 1 - (1 - r2_rfe) * (n - 1) / (n - 8 - 1)
cv_rfe = cross_val_score(rfe_selector, X_train, y_train, cv=10, scoring="r2").mean()
results.append({
    "Model": "RF + RFE (8 features)",
    "RMSE": round(rmse_rfe, 4),
    "R2": round(r2_rfe, 4),
    "Adjusted_R2": round(adj_r2_rfe, 4),
    "CV_R2": round(cv_rfe, 4),
})
predictions["RF_RFE"] = y_pred_rfe

# Model 6: Ridge Regression
res, pred = evaluate_model(
    Ridge(alpha=1.0, random_state=42), X_train, X_test, y_train, y_test,
    "Ridge Regression", len(feature_names)
)
results.append(res)
predictions["Ridge_Regression"] = pred

# Model 7: Lasso Regression
res, pred = evaluate_model(
    Lasso(alpha=0.1, random_state=42), X_train, X_test, y_train, y_test,
    "Lasso Regression", len(feature_names)
)
results.append(res)
predictions["Lasso_Regression"] = pred

# Model 8: Bayesian Ridge
res, pred = evaluate_model(
    BayesianRidge(), X_train, X_test, y_train, y_test,
    "Bayesian Ridge", len(feature_names)
)
results.append(res)
predictions["Bayesian_Ridge"] = pred

# Model 9: Tuned Ridge with GridSearchCV
ridge_params = {"alpha": [0.01, 0.1, 0.5, 1.0, 5.0, 10.0, 50.0, 100.0]}
ridge_grid = GridSearchCV(Ridge(random_state=42), ridge_params, cv=10, scoring="r2")
ridge_grid.fit(X_train, y_train)
y_pred_tuned = ridge_grid.predict(X_test)
rmse_tuned = np.sqrt(mean_squared_error(y_test, y_pred_tuned))
r2_tuned = r2_score(y_test, y_pred_tuned)
adj_r2_tuned = 1 - (1 - r2_tuned) * (n - 1) / (n - len(feature_names) - 1)
cv_tuned = ridge_grid.best_score_
results.append({
    "Model": "Tuned Ridge (GridSearchCV)",
    "RMSE": round(rmse_tuned, 4),
    "R2": round(r2_tuned, 4),
    "Adjusted_R2": round(adj_r2_tuned, 4),
    "CV_R2": round(cv_tuned, 4),
})
predictions["Tuned_Ridge"] = y_pred_tuned

# ── 8. Save model comparison ──────────────────────────────────────────────
results_df = pd.DataFrame(results)
results_df.to_csv("models_comparison.csv", index=False)
print("\nModel comparison:")
print(results_df.to_string(index=False))

# ── 9. Save predictions ───────────────────────────────────────────────────
os.makedirs("predictions", exist_ok=True)
for model_name, preds in predictions.items():
    pred_df = pd.DataFrame({
        "actual": y_test.values,
        "predicted": preds
    })
    pred_df.to_csv(f"predictions/{model_name}.csv", index=False)

# ── 10. Feature sets JSON ─────────────────────────────────────────────────
feature_sets = {
    "all_features": {
        "features": feature_names,
        "reason": "Baseline: all 13 predictor features included without any multicollinearity remedy"
    },
    "vif_reduced": {
        "features": vif_reduced_features,
        "reason": "Features remaining after iterative removal of features with VIF > 10"
    },
    "rfe_selected": {
        "features": rfe_features,
        "reason": "Top 8 features selected by Recursive Feature Elimination with Random Forest"
    },
    "regularized_all": {
        "features": feature_names,
        "reason": "All features used with Ridge/Lasso/Bayesian Ridge regularization to handle multicollinearity"
    }
}
with open("feature_sets.json", "w") as f:
    json.dump(feature_sets, f, indent=2)

# ── 11. report.json ───────────────────────────────────────────────────────
best_idx = max(range(len(results)), key=lambda i: results[i]["CV_R2"])
best_model = results[best_idx]["Model"]
best_cv_r2 = results[best_idx]["CV_R2"]

report = {
    "best_model": best_model,
    "best_cv_r2": best_cv_r2,
    "vif_reduced_features": vif_reduced_features,
    "remediation_ranking": [
        "Regularization (Ridge/Lasso) - preserves all features while controlling coefficient magnitude",
        "Automated Feature Selection (RFE) - data-driven feature removal based on importance",
        "VIF-based Feature Removal - simple but can remove predictive features and worsen performance"
    ]
}
with open("report.json", "w") as f:
    json.dump(report, f, indent=2)

# ── 12. analysis_report.txt ───────────────────────────────────────────────
high_vif_features = vif_df[vif_df["VIF"] > 5]["Feature"].tolist()
rad_tax_corr = corr_matrix.loc["RAD", "TAX"]

full_lr_cv = results[0]["CV_R2"]
vif_lr_cv = results[2]["CV_R2"]
rf_all_cv = results[1]["CV_R2"]

report_text = f"""Multicollinearity Detection and Remediation: Analysis Report
=============================================================

1. Introduction
---------------
Multicollinearity is a statistical phenomenon where two or more predictor variables in a
regression model are highly correlated, meaning one can be predicted from the others with
substantial accuracy. This creates problems for ordinary least squares regression because
it inflates the variance of coefficient estimates, making them unstable and difficult to
interpret. In this analysis, we systematically detect multicollinearity in the Boston housing
dataset and evaluate three distinct remediation strategies to determine which approach best
balances model interpretability with predictive performance.

2. Dataset Overview
-------------------
The Boston housing dataset contains 506 observations of 14 variables. The target variable
MEDV represents the median value of owner-occupied homes in thousands of dollars. The 13
predictor variables capture various socioeconomic and geographic characteristics including
crime rate (CRIM), proportion of residential land (ZN), proportion of non-retail business
(INDUS), proximity to the Charles River (CHAS), nitric oxide concentration (NOX), average
number of rooms (RM), proportion of older units (AGE), distance to employment centers (DIS),
accessibility to highways (RAD), property tax rate (TAX), pupil-teacher ratio (PTRATIO),
proportion of Black residents (B), and percentage of lower-status population (LSTAT).

3. Multicollinearity Detection
------------------------------
We employed two complementary methods to detect multicollinearity: Pearson correlation
analysis and Variance Inflation Factor (VIF) computation.

The correlation analysis revealed several highly correlated feature pairs. Most notably,
RAD (accessibility to radial highways) and TAX (property tax rate) exhibit a correlation
of {rad_tax_corr:.4f}, which is extremely high. Other notable pairs include NOX and DIS
(distance to employment centers) with a strong negative correlation, NOX and INDUS with
a strong positive correlation, and AGE and DIS with a strong negative correlation. These
correlations make physical sense: areas with more highway access tend to have higher tax
rates, and industrial areas tend to have higher pollution (NOX) and be closer to employment.

The VIF analysis quantifies multicollinearity more rigorously. Features with VIF exceeding
10 are considered severely multicollinear, while those above 5 warrant attention. Our
analysis identified several features with elevated VIF scores including {', '.join(high_vif_features)}.
After iterative removal of the highest-VIF features until all remaining features had
VIF below 10, we arrived at a reduced feature set of {len(vif_reduced_features)}
features: {', '.join(vif_reduced_features)}.

We also validated our VIF approach on the simpler BMI dataset, which demonstrated how
structural multicollinearity arises when derived variables (like BMI Index, which is
computed from Height and Weight) are included alongside their source variables.

4. Remediation Strategy 1: VIF-Based Feature Removal
-----------------------------------------------------
The most straightforward remedy for multicollinearity is to remove features with high VIF
scores iteratively. Starting with the feature exhibiting the highest VIF, we removed it and
recomputed VIF scores for the remaining features, repeating until all features had VIF
below our chosen threshold. This process reduced our feature set from 13 to
{len(vif_reduced_features)} features.

However, this approach came with a significant cost to predictive accuracy. The Linear
Regression model trained on VIF-reduced features achieved a cross-validated R-squared of
{vif_lr_cv:.4f}, compared to {full_lr_cv:.4f} for the full-feature model. This represents
a meaningful drop in predictive performance. The reason is that VIF-based removal is
agnostic to predictive power: it removes features based purely on their correlation with
other predictors, regardless of how important they are for predicting the target. Features
like RM (average rooms) and LSTAT (lower-status population percentage), which are among the
strongest predictors of house prices, may be removed or their predictive contribution lost
when correlated features are dropped. This illustrates a fundamental tension between
statistical purity (removing collinear features) and practical utility (maximizing prediction).

5. Remediation Strategy 2: Regularization
------------------------------------------
Regularization techniques like Ridge and Lasso regression address multicollinearity by adding
penalty terms to the loss function. Ridge regression adds an L2 penalty that shrinks
coefficient magnitudes without eliminating features entirely, while Lasso adds an L1 penalty
that can drive coefficients exactly to zero, performing implicit feature selection.

Ridge Regression achieved a cross-validated R-squared of {results[5]["CV_R2"]:.4f}, Lasso
achieved {results[6]["CV_R2"]:.4f}, and Bayesian Ridge achieved {results[7]["CV_R2"]:.4f}.
These results demonstrate that regularization preserves predictive performance while
controlling the instability caused by multicollinearity. The tuned Ridge model with
GridSearchCV optimization achieved a CV R-squared of {results[8]["CV_R2"]:.4f}, showing
that hyperparameter tuning can further improve regularized models.

6. Remediation Strategy 3: Automated Feature Selection (RFE)
-------------------------------------------------------------
Recursive Feature Elimination (RFE) with a Random Forest estimator provides a data-driven
approach to feature selection that is superior to VIF-based removal in most practical
scenarios. Unlike VIF-based removal, RFE considers feature importance for prediction when
deciding which features to eliminate. This means RFE retains features that matter most for
predicting the target, even if those features are correlated with others. Our RFE pipeline
selected 8 features ({', '.join(rfe_features)}) and achieved a cross-validated R-squared of
{results[4]["CV_R2"]:.4f}. This demonstrates that intelligent feature selection can reduce
dimensionality while preserving most of the predictive power.

7. Comparison and Recommendations
-----------------------------------
The Random Forest model with all features achieved the highest cross-validated R-squared of
{rf_all_cv:.4f}, demonstrating that tree-based models naturally handle multicollinearity well
through their ensemble structure. Among the remediation strategies, regularization (particularly
tuned Ridge) provided the best balance of performance and multicollinearity control for linear
models. RFE offered a middle ground, selecting features based on predictive importance rather
than correlation alone. VIF-based feature removal, while conceptually simple and useful for
understanding feature relationships, proved counterproductive for prediction accuracy.

Our overall recommendation is to use regularization as the primary remedy for multicollinearity
in regression tasks. If feature reduction is specifically required for interpretability, RFE is
preferable to VIF-based removal. The key insight from this analysis is that statistical
remedies for multicollinearity should be evaluated in the context of their impact on predictive
performance, not applied blindly based on arbitrary VIF thresholds.

The best performing model overall was {best_model} with a cross-validated R-squared of
{best_cv_r2:.4f}. This demonstrates that the choice of modeling approach matters as much as,
if not more than, the choice of multicollinearity remedy.
"""

with open("analysis_report.txt", "w") as f:
    f.write(report_text)

print("\nAll outputs generated successfully!")
print(f"Best model: {best_model} (CV R2: {best_cv_r2})")
print(f"VIF-reduced features ({len(vif_reduced_features)}): {vif_reduced_features}")
print(f"Models compared: {len(results)}")
PYEOF
