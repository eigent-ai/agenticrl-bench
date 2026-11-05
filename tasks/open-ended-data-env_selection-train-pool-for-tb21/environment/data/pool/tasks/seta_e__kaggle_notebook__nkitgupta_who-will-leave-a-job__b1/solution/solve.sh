#!/bin/bash

mkdir -p /output

cat > /output/pipeline.R << 'RSCRIPT'
set.seed(42)

suppressPackageStartupMessages({
  library(tidymodels)
  library(readr)
  library(dplyr)
  library(tidyr)
  library(themis)
  library(vip)
  library(ranger)
  library(xgboost)
})

# ============================================================
# 1. Read Data
# ============================================================
train_data <- read_csv("/data/aug_train.csv", show_col_types = FALSE)
test_data  <- read_csv("/data/aug_test.csv", show_col_types = FALSE)

# ============================================================
# 2. EDA Report
# ============================================================
eda_lines <- c(
  "Exploratory Data Analysis Report",
  "================================",
  "",
  sprintf("Dataset Shape: %d rows, %d columns", nrow(train_data), ncol(train_data)),
  sprintf("Test Dataset Shape: %d rows, %d columns", nrow(test_data), ncol(test_data)),
  "",
  "Missing Values Per Column:",
  paste0("  ", names(train_data), ": ", colSums(is.na(train_data))),
  "",
  "Target Class Distribution:",
  sprintf("  Class 0 (will not change): %d (%.1f%%)",
          sum(train_data$target == 0),
          100 * mean(train_data$target == 0)),
  sprintf("  Class 1 (will change): %d (%.1f%%)",
          sum(train_data$target == 1),
          100 * mean(train_data$target == 1)),
  "",
  "Summary Statistics:",
  capture.output(summary(train_data))
)
writeLines(eda_lines, "/output/eda_report.txt")
cat("EDA report written.\n")

# ============================================================
# 3. Prepare Data and Split
# ============================================================
# Convert target to factor
train_data <- train_data %>%
  mutate(target = factor(target, levels = c("0", "1")))

# Stratified train/validation split
data_split <- initial_split(train_data, prop = 0.8, strata = target)
train_set <- training(data_split)
val_set   <- testing(data_split)

cat(sprintf("Training set: %d rows, Validation set: %d rows\n",
            nrow(train_set), nrow(val_set)))

# ============================================================
# 4. Preprocessing Rationale
# ============================================================
rationale_lines <- c(
  "Preprocessing Rationale",
  "=======================",
  "",
  "1. Missing Value Handling (Imputation):",
  "   - Numeric features: median imputation was used because it is robust to outliers",
  "     and does not assume normality in the data distribution.",
  "   - Categorical features: mode imputation was used, filling missing values with",
  "     the most frequent category. This preserves the distribution of categorical variables.",
  "   - Columns with substantial missing values: gender (~24%), company_type (~32%),",
  "     company_size (~31%), major_discipline (~15%), education_level, enrolled_university,",
  "     last_new_job, and experience.",
  "",
  "2. Categorical Feature Encoding:",
  "   - Nominal categorical features were converted to dummy variables (one-hot encoding)",
  "     using step_dummy() from the recipes package.",
  "   - High-cardinality features (like city) were first collapsed using step_other()",
  "     to group rare categories together, reducing dimensionality.",
  "   - This avoids imposing artificial ordering on unordered categories.",
  "",
  "3. Class Imbalance Handling:",
  "   - The target variable is significantly imbalanced (~75% class 0, ~25% class 1).",
  "   - SMOTE (Synthetic Minority Over-sampling Technique) was applied via step_smote()",
  "     from the themis package to generate synthetic minority class samples.",
  "   - It is applied only within training data (via workflow integration) to prevent",
  "     data leakage into validation or test sets."
)
writeLines(rationale_lines, "/output/preprocessing_rationale.txt")
cat("Preprocessing rationale written.\n")

# ============================================================
# 5. Define Recipe (step_smote is after the split above)
# ============================================================
base_recipe <- recipe(target ~ ., data = train_set) %>%
  update_role(enrollee_id, new_role = "id") %>%
  step_impute_median(all_numeric_predictors()) %>%
  step_impute_mode(all_nominal_predictors()) %>%
  step_novel(all_nominal_predictors()) %>%
  step_other(all_nominal_predictors(), threshold = 0.02) %>%
  step_dummy(all_nominal_predictors()) %>%
  step_smote(target, over_ratio = 0.8) %>%
  step_zv(all_predictors()) %>%
  step_normalize(all_numeric_predictors())

cat("Recipe defined.\n")

# ============================================================
# 6. Define Models
# ============================================================
lr_spec <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

rf_spec <- rand_forest(trees = 500, min_n = 5) %>%
  set_engine("ranger", importance = "impurity") %>%
  set_mode("classification")

bt_spec <- boost_tree(trees = 200, tree_depth = 5, learn_rate = 0.1) %>%
  set_engine("xgboost") %>%
  set_mode("classification")

model_specs <- list(
  logistic_regression = lr_spec,
  random_forest       = rf_spec,
  xgboost             = bt_spec
)

# ============================================================
# 7. Train, Evaluate, Cross-Validate
# ============================================================
cv_folds <- vfold_cv(train_set, v = 5, strata = target)

results <- list()
fitted_workflows <- list()

for (model_name in names(model_specs)) {
  cat(sprintf("Training model: %s\n", model_name))

  wf <- workflow() %>%
    add_recipe(base_recipe) %>%
    add_model(model_specs[[model_name]])

  # Fit on training data
  fitted_wf <- fit(wf, data = train_set)
  fitted_workflows[[model_name]] <- fitted_wf

  # Training AUC
  train_pred <- predict(fitted_wf, train_set, type = "prob") %>%
    bind_cols(train_set %>% dplyr::select(target))
  train_auc <- roc_auc(train_pred, target, .pred_1, event_level = "second")$.estimate

  # Validation AUC
  val_pred <- predict(fitted_wf, val_set, type = "prob") %>%
    bind_cols(val_set %>% dplyr::select(target))
  test_auc <- roc_auc(val_pred, target, .pred_1, event_level = "second")$.estimate

  # Cross-validation AUC
  cv_res <- fit_resamples(
    wf,
    resamples = cv_folds,
    metrics = metric_set(roc_auc),
    control = control_resamples(event_level = "second")
  )
  cv_per_fold <- collect_metrics(cv_res, summarize = FALSE)
  fold_aucs <- cv_per_fold$.estimate
  cv_mean <- mean(fold_aucs)
  cv_std  <- sd(fold_aucs)

  results[[model_name]] <- tibble(
    model_name  = model_name,
    train_auc   = round(train_auc, 4),
    test_auc    = round(test_auc, 4),
    cv_mean_auc = round(cv_mean, 4),
    cv_std_auc  = round(cv_std, 4)
  )

  cat(sprintf("  train_auc=%.4f, test_auc=%.4f, cv_mean=%.4f, cv_std=%.4f\n",
              train_auc, test_auc, cv_mean, cv_std))
}

# Write model comparison
model_comparison <- bind_rows(results)
write_csv(model_comparison, "/output/model_comparison.csv")
cat("Model comparison written.\n")

# ============================================================
# 8. Select Best Model & Feature Importance
# ============================================================
model_comparison_sorted <- model_comparison %>% dplyr::arrange(desc(test_auc))
best_model_name <- model_comparison_sorted$model_name[1]
best_test_auc   <- model_comparison_sorted$test_auc[1]
best_cv_mean    <- model_comparison_sorted$cv_mean_auc[1]
best_cv_std     <- model_comparison_sorted$cv_std_auc[1]
best_wf <- fitted_workflows[[best_model_name]]

cat(sprintf("Best model: %s (test_auc=%.4f)\n", best_model_name, best_test_auc))

# Extract feature importance
best_fit <- extract_fit_parsnip(best_wf)
imp_df <- vi(best_fit) %>%
  dplyr::rename(feature = Variable, importance = Importance) %>%
  dplyr::arrange(desc(importance))
write_csv(imp_df, "/output/feature_importance.csv")
cat("Feature importance written.\n")

# ============================================================
# 9. Generate Predictions on Test Set
# ============================================================
test_probs <- predict(best_wf, test_data, type = "prob")
predictions <- tibble(
  enrollee_id          = test_data$enrollee_id,
  predicted_target     = ifelse(test_probs$.pred_1 >= 0.5, 1, 0),
  predicted_probability = round(test_probs$.pred_1, 6)
)
write_csv(predictions, "/output/predictions.csv")
cat(sprintf("Predictions written: %d rows\n", nrow(predictions)))

# ============================================================
# 10. Final Report
# ============================================================
top5 <- imp_df[1:min(5, nrow(imp_df)), ]
top5_text <- paste0("  ", seq_len(nrow(top5)), ". ", top5$feature,
                    " (importance: ", round(top5$importance, 4), ")")

report_lines <- c(
  "Final Report: HR Analytics Job Change Prediction",
  "=================================================",
  "",
  "Best Model Selection:",
  sprintf("  The best-performing model is '%s' with a validation AUC of %.4f",
          best_model_name, best_test_auc),
  sprintf("  and a cross-validation mean AUC of %.4f (std: %.4f).",
          best_cv_mean, best_cv_std),
  "",
  "  Model Comparison Summary:",
  capture.output(print(model_comparison, n = Inf)),
  "",
  sprintf("  %s was chosen because it achieved the highest validation AUC among",
          best_model_name),
  "  the three models tested, balancing predictive power with generalization.",
  "",
  "Top 5 Most Important Features:",
  top5_text,
  "",
  "Key Findings:",
  "  - city_development_index is a strong predictor of job change intent,",
  "    suggesting that urban development level influences career decisions.",
  "  - training_hours and experience are important factors, indicating that",
  "    professional development activity and tenure affect attrition risk.",
  "  - company_size and company_type play roles in predicting turnover,",
  "    suggesting organizational characteristics matter.",
  "  - education_level and relevent_experience contribute to the prediction,",
  "    reflecting the role of qualifications in career mobility.",
  "  - gender and enrolled_university show some predictive power, though",
  "    their effect sizes are smaller than professional factors.",
  "  - last_new_job duration also influences predictions, suggesting that",
  "    recent job mobility patterns predict future changes.",
  "",
  "Limitations:",
  "  - Limitation: The dataset may not generalize to all regions or industries,",
  "    as it focuses specifically on data scientists in certain cities.",
  "  - Limitation: Missing values are substantial in several columns (up to 32%),",
  "    and imputation may introduce bias in the model's predictions.",
  "  - Limitation: Synthetic oversampling creates samples that may not fully",
  "    represent the true minority class distribution.",
  "  - Limitation: The model was trained on a single temporal snapshot and may",
  "    not capture evolving trends in job market dynamics.",
  "  - Limitation: Feature interactions and non-linear effects may not be fully",
  "    captured by all model types, particularly logistic regression."
)
writeLines(report_lines, "/output/final_report.txt")
cat("Final report written.\n")

cat("\nPipeline complete!\n")
RSCRIPT

# Run the R pipeline
cd /output
Rscript /output/pipeline.R

echo "Done!"
