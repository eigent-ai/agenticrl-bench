generate_report <- function(results) {
  cat(strrep("=", 50), "\n")
  cat("EVALUATION REPORT\n")
  cat(strrep("=", 50), "\n")

  fold_scores <- results$fold_scores
  n_folds <- length(fold_scores)
  cat(sprintf("Number of folds: %d\n", n_folds))
  cat(sprintf("Score range: %.4f - %.4f\n", fold_scores[[1]], fold_scores[[n_folds]]))
  cat(sprintf("Mean CV Score: %.4f\n", results$mean_cv_score))
  cat(sprintf("Std CV Score: %.4f\n", results$std_cv_score))

  cat(sprintf("\nTest Accuracy: %.4f\n", results$prediction_accuracy))
  cat(sprintf("Total folds configured: %d\n", results$total_folds))

  cat(strrep("=", 50), "\n")
}
