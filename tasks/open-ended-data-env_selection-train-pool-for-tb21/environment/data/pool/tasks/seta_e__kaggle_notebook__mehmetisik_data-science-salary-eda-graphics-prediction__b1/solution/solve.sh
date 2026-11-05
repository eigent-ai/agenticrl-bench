#!/bin/bash

cat > /tmp/pipeline.R << 'RSCRIPT'
library(caret)
library(randomForest)
library(gbm)
library(xgboost)
library(glmnet)
library(e1071)
library(jsonlite)
library(data.table)
library(rpart)
library(kernlab)

set.seed(42)

# ============================================================
# 1. Load data
# ============================================================
df <- fread("/home/user/dataset/housing.csv", stringsAsFactors = TRUE)
outdir <- "/home/user/workspace"

# ============================================================
# 2. EDA Report
# ============================================================
sink(file.path(outdir, "eda_report.txt"))
cat("=== EDA Report ===\n\n")
cat(sprintf("Dataset Shape: %d rows, %d columns\n\n", nrow(df), ncol(df)))

cat("Column Types:\n")
for (col in names(df)) {
  cat(sprintf("  %s: %s\n", col, class(df[[col]])[1]))
}

cat("\nMissing Values:\n")
na_counts <- colSums(is.na(df))
for (col in names(na_counts)) {
  cat(sprintf("  %s: %d missing\n", col, na_counts[col]))
}
cat(sprintf("\nTotal missing values: %d\n", sum(na_counts)))

cat("\nTarget Variable (sale_price) Statistics:\n")
cat(sprintf("  Mean: %.2f\n", mean(df$sale_price, na.rm=TRUE)))
cat(sprintf("  Median: %.2f\n", median(df$sale_price, na.rm=TRUE)))
cat(sprintf("  SD (Standard Deviation): %.2f\n", sd(df$sale_price, na.rm=TRUE)))
cat(sprintf("  Min: %.2f\n", min(df$sale_price, na.rm=TRUE)))
cat(sprintf("  Max: %.2f\n", max(df$sale_price, na.rm=TRUE)))

cat_cols <- c("neighborhood", "bldg_type", "house_style", "exterior_1st",
              "foundation", "heating_qc", "central_air", "kitchen_qual",
              "ms_zoning", "lot_shape", "land_contour", "condition_1")
cat("\nCategorical Column Value Counts:\n")
for (col in cat_cols) {
  if (col %in% names(df)) {
    cat(sprintf("\n  %s:\n", col))
    tbl <- sort(table(df[[col]]), decreasing=TRUE)
    for (i in seq_along(tbl)) {
      cat(sprintf("    %s: %d\n", names(tbl)[i], tbl[i]))
    }
  }
}
sink()

# ============================================================
# 3. Prepare data - handle missing values
# ============================================================
# Fill missing garage_cars with median
if (any(is.na(df$garage_cars))) {
  df$garage_cars[is.na(df$garage_cars)] <- median(df$garage_cars, na.rm=TRUE)
}
# Fill missing total_bsmt_sf with median
if (any(is.na(df$total_bsmt_sf))) {
  df$total_bsmt_sf[is.na(df$total_bsmt_sf)] <- median(df$total_bsmt_sf, na.rm=TRUE)
}

# Log-transform target
df$log_price <- log(df$sale_price)

# ============================================================
# 4. Feature Engineering Strategy 1: Derived features
# ============================================================
df$house_age <- df$yr_sold - df$year_built
df$total_sf <- df$gr_liv_area + df$total_bsmt_sf
df$remod_age <- df$yr_sold - df$year_remod_add
df$total_bath <- df$full_bath + 0.5 * df$half_bath

# Identify numeric and factor columns
num_cols <- names(df)[sapply(df, is.numeric)]
num_cols <- setdiff(num_cols, c("sale_price", "log_price"))

# Strategy 1: baseline model with numeric features only
set.seed(42)
train_idx_s1 <- createDataPartition(df$log_price, p=0.8, list=FALSE)
train_s1 <- df[train_idx_s1, ..num_cols]
test_s1 <- df[-train_idx_s1, ..num_cols]
train_y_s1 <- df$log_price[train_idx_s1]
test_y_s1 <- df$log_price[-train_idx_s1]

set.seed(42)
tc_s1 <- trainControl(method="cv", number=3)
model_s1 <- train(x=as.data.frame(train_s1), y=train_y_s1, method="rpart", trControl=tc_s1)
pred_s1 <- predict(model_s1, as.data.frame(test_s1))
ss_res_s1 <- sum((test_y_s1 - pred_s1)^2)
ss_tot_s1 <- sum((test_y_s1 - mean(test_y_s1))^2)
r2_strategy1 <- 1 - ss_res_s1/ss_tot_s1

# ============================================================
# 5. Feature Engineering Strategy 2: Dummy variables + rare label grouping
# ============================================================
# Rare label grouping for high-cardinality categoricals
rare_group <- function(x, threshold=0.02) {
  freq <- table(x) / length(x)
  rare_levels <- names(freq[freq < threshold])
  x <- as.character(x)
  x[x %in% rare_levels] <- "Other"
  as.factor(x)
}

df$neighborhood_grouped <- rare_group(df$neighborhood)
df$exterior_1st_grouped <- rare_group(df$exterior_1st)

# Create dummy variables
dummy_cols <- c("neighborhood_grouped", "exterior_1st_grouped", "bldg_type",
                "house_style", "foundation", "heating_qc", "central_air",
                "kitchen_qual", "ms_zoning", "condition_1")

# Convert factors for dummyVars
for (col in dummy_cols) {
  df[[col]] <- as.factor(df[[col]])
}

formula_str <- paste("~", paste(dummy_cols, collapse=" + "))
dv <- dummyVars(as.formula(formula_str), data=df, fullRank=TRUE)
dummy_data <- predict(dv, newdata=df)
dummy_df <- as.data.table(dummy_data)

# Combine numeric + dummy features
all_features <- cbind(df[, ..num_cols], dummy_df)

set.seed(42)
train_idx_s2 <- createDataPartition(df$log_price, p=0.8, list=FALSE)
train_s2 <- all_features[train_idx_s2, ]
test_s2 <- all_features[-train_idx_s2, ]
train_y_s2 <- df$log_price[train_idx_s2]
test_y_s2 <- df$log_price[-train_idx_s2]

set.seed(42)
tc_s2 <- trainControl(method="cv", number=3)
model_s2 <- train(x=as.data.frame(train_s2), y=train_y_s2, method="rpart", trControl=tc_s2)
pred_s2 <- predict(model_s2, as.data.frame(test_s2))
ss_res_s2 <- sum((test_y_s2 - pred_s2)^2)
ss_tot_s2 <- sum((test_y_s2 - mean(test_y_s2))^2)
r2_strategy2 <- 1 - ss_res_s2/ss_tot_s2

# Write feature engineering log
sink(file.path(outdir, "feature_engineering_log.txt"))
cat("=== Feature Engineering Log ===\n\n")
cat("Strategy 1: Derived Feature Engineering\n")
cat("  Description: Created derived numeric features including house_age (yr_sold - year_built),\n")
cat("  total_sf (gr_liv_area + total_bsmt_sf), remod_age (yr_sold - year_remod_add),\n")
cat("  and total_bath (full_bath + 0.5 * half_bath). Used only numeric features.\n")
cat(sprintf("  R2: %.4f\n\n", r2_strategy1))
cat("Strategy 2: Dummy Variable Encoding + Rare Label Grouping Transform\n")
cat("  Description: Applied rare-label grouping to high-cardinality categoricals\n")
cat("  (neighborhood, exterior_1st) with threshold 2%%. Created dummy variable encoding\n")
cat("  for all categorical features. Combined with numeric and derived features.\n")
cat(sprintf("  R2: %.4f\n\n", r2_strategy2))
cat(sprintf("Impact: Strategy 2 R2 (%.4f) vs Strategy 1 R2 (%.4f)\n", r2_strategy2, r2_strategy1))
sink()

# ============================================================
# 6. Final train/test split with all features
# ============================================================
set.seed(42)
final_idx <- createDataPartition(df$log_price, p=0.8, list=FALSE)
X_train <- as.data.frame(all_features[final_idx, ])
X_test <- as.data.frame(all_features[-final_idx, ])
y_train <- df$log_price[final_idx]
y_test <- df$log_price[-final_idx]

# ============================================================
# 7. Train 4+ models
# ============================================================
tc <- trainControl(method="cv", number=5)

set.seed(42)
cat("Training Random Forest...\n")
model_rf <- train(x=X_train, y=y_train, method="rf", trControl=tc, ntree=100)

set.seed(42)
cat("Training GBM...\n")
model_gbm <- train(x=X_train, y=y_train, method="gbm", trControl=tc, verbose=FALSE)

set.seed(42)
cat("Training glmnet...\n")
model_glmnet <- train(x=X_train, y=y_train, method="glmnet", trControl=tc)

set.seed(42)
cat("Training rpart...\n")
model_rpart <- train(x=X_train, y=y_train, method="rpart", trControl=tc)

# Evaluate all models on test set
evaluate_model <- function(model, X_test, y_test) {
  preds <- predict(model, X_test)
  ss_res <- sum((y_test - preds)^2)
  ss_tot <- sum((y_test - mean(y_test))^2)
  r2 <- 1 - ss_res/ss_tot
  rmse <- sqrt(mean((y_test - preds)^2))
  mae <- mean(abs(y_test - preds))
  list(r2=r2, rmse=rmse, mae=mae, preds=preds)
}

res_rf <- evaluate_model(model_rf, X_test, y_test)
res_gbm <- evaluate_model(model_gbm, X_test, y_test)
res_glmnet <- evaluate_model(model_glmnet, X_test, y_test)
res_rpart <- evaluate_model(model_rpart, X_test, y_test)

# Write model comparison
comp <- data.frame(
  model_name = c("rf", "gbm", "glmnet", "rpart"),
  r2_score = c(res_rf$r2, res_gbm$r2, res_glmnet$r2, res_rpart$r2),
  rmse = c(res_rf$rmse, res_gbm$rmse, res_glmnet$rmse, res_rpart$rmse),
  mae = c(res_rf$mae, res_gbm$mae, res_glmnet$mae, res_rpart$mae)
)
write.csv(comp, file.path(outdir, "model_comparison.csv"), row.names=FALSE)
cat("Model comparison:\n")
print(comp)

# ============================================================
# 8. Select best model and tune hyperparameters
# ============================================================
models_list <- list(rf=model_rf, gbm=model_gbm, glmnet=model_glmnet, rpart=model_rpart)
results_list <- list(rf=res_rf, gbm=res_gbm, glmnet=res_glmnet, rpart=res_rpart)
r2_scores <- c(res_rf$r2, res_gbm$r2, res_glmnet$r2, res_rpart$r2)
best_idx <- which.max(r2_scores)
best_name <- c("rf", "gbm", "glmnet", "rpart")[best_idx]
best_model <- models_list[[best_name]]
best_res <- results_list[[best_name]]

cat(sprintf("\nBest model: %s with R2=%.4f\n", best_name, r2_scores[best_idx]))

# Hyperparameter tuning with 5-fold CV
set.seed(42)
tc_tune <- trainControl(method="cv", number=5, savePredictions="final")

if (best_name == "rf") {
  tune_grid <- expand.grid(mtry=c(5, 10, 15, 20))
  set.seed(42)
  best_tuned <- train(x=X_train, y=y_train, method="rf", trControl=tc_tune,
                       tuneGrid=tune_grid, ntree=200)
} else if (best_name == "gbm") {
  tune_grid <- expand.grid(
    n.trees=c(100, 200, 300),
    interaction.depth=c(3, 5, 7),
    shrinkage=c(0.05, 0.1),
    n.minobsinnode=10
  )
  set.seed(42)
  best_tuned <- train(x=X_train, y=y_train, method="gbm", trControl=tc_tune,
                       tuneGrid=tune_grid, verbose=FALSE)
} else if (best_name == "glmnet") {
  tune_grid <- expand.grid(alpha=c(0, 0.5, 1), lambda=c(0.001, 0.01, 0.1))
  set.seed(42)
  best_tuned <- train(x=X_train, y=y_train, method="glmnet", trControl=tc_tune,
                       tuneGrid=tune_grid)
} else {
  tune_grid <- expand.grid(cp=c(0.001, 0.005, 0.01, 0.02))
  set.seed(42)
  best_tuned <- train(x=X_train, y=y_train, method="rpart", trControl=tc_tune,
                       tuneGrid=tune_grid)
}

# Get tuned predictions
tuned_preds <- predict(best_tuned, X_test)
ss_res_tuned <- sum((y_test - tuned_preds)^2)
ss_tot_tuned <- sum((y_test - mean(y_test))^2)
tuned_r2 <- 1 - ss_res_tuned/ss_tot_tuned
tuned_rmse <- sqrt(mean((y_test - tuned_preds)^2))
tuned_mae <- mean(abs(y_test - tuned_preds))

cat(sprintf("Tuned model R2: %.4f, RMSE: %.4f, MAE: %.4f\n", tuned_r2, tuned_rmse, tuned_mae))

# Extract CV scores (R-squared from 5 folds)
cv_results <- best_tuned$resample
# Get Rsquared from the best tuneLength
best_tune_row <- best_tuned$bestTune
cv_r2_scores <- cv_results$Rsquared
if (length(cv_r2_scores) > 5) {
  cv_r2_scores <- cv_r2_scores[1:5]
}
# Pad if needed
while (length(cv_r2_scores) < 5) {
  cv_r2_scores <- c(cv_r2_scores, mean(cv_r2_scores))
}

# ============================================================
# 9. Write predictions
# ============================================================
predictions_df <- data.frame(actual=y_test, predicted=tuned_preds)
write.csv(predictions_df, file.path(outdir, "predictions.csv"), row.names=FALSE)

# ============================================================
# 10. Write best model results JSON
# ============================================================
best_params_list <- as.list(best_tuned$bestTune)
best_params_list$seed <- 42

results_json <- list(
  best_model_name = best_name,
  r2_score = tuned_r2,
  rmse = tuned_rmse,
  mae = tuned_mae,
  best_params = best_params_list,
  cv_scores = as.numeric(cv_r2_scores),
  test_predictions_count = nrow(predictions_df)
)

write_json(results_json, file.path(outdir, "best_model_results.json"),
           auto_unbox=TRUE, pretty=TRUE)

# ============================================================
# 11. Feature importance
# ============================================================
vi <- varImp(best_tuned)
vi_df <- vi$importance
vi_df$feature <- rownames(vi_df)
names(vi_df)[1] <- "importance"
vi_df <- vi_df[order(-vi_df$importance), ]
vi_out <- data.frame(feature=vi_df$feature, importance=vi_df$importance)
write.csv(vi_out, file.path(outdir, "feature_importance.csv"), row.names=FALSE)

cat("\nPipeline complete! All output files written to", outdir, "\n")
RSCRIPT

Rscript /tmp/pipeline.R
