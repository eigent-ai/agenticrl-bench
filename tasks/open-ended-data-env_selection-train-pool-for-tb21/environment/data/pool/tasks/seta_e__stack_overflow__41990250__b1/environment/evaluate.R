#!/usr/bin/env Rscript
# Regression evaluation script
# Reads predicted and actual values, computes regression metrics,
# and writes results to a JSON file.

library(jsonlite)

evaluate <- function(predictions_path, actuals_path, output_path) {
  # Load data
  predictions <- read.csv(predictions_path)
  actuals <- read.csv(actuals_path)

  pred <- predictions[, 1]
  actual <- actuals[, 1]

  n <- length(actual)

  # Compute residuals
  residuals <- actual - pred

  # RMSE (Root Mean Squared Error)
  rmse <- sqrt(mean(residuals^2))

  # MAE (Mean Absolute Error)
  mae <- mean(abs(residuals))

  # MAPE (Mean Absolute Percentage Error)
  mape <- mean(abs((actual - pred) / actual)) * 100

  # R-squared (coefficient of determination)
  r_squared <- cor(pred, actual)^2

  result <- list(
    rmse = rmse,
    mae = mae,
    mape = mape,
    r_squared = r_squared
  )

  write_json(result, output_path, auto_unbox = TRUE, pretty = TRUE)
  cat("Results written to", output_path, "\n")
  cat("  RMSE:", rmse, "\n")
  cat("  MAE:", mae, "\n")
  cat("  MAPE:", mape, "%\n")
  cat("  R-squared:", r_squared, "\n")
}

evaluate("data/predictions.csv", "data/actuals.csv", "results.json")
