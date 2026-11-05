combined <- readRDS("combined_history.rds")

metric_keys <- names(combined)[names(combined) != "epoch"]
total_epochs <- length(combined[[metric_keys[1]]])

# Build JSON output using base R (no external packages needed)
json <- sprintf(paste0(
  '{\n',
  '  "total_epochs": %d,\n',
  '  "metrics": ["%s"],\n',
  '  "final_loss": %.6f,\n',
  '  "final_val_loss": %.6f,\n',
  '  "final_accuracy": %.6f,\n',
  '  "final_val_accuracy": %.6f,\n',
  '  "min_loss": %.6f,\n',
  '  "max_accuracy": %.6f\n',
  '}'
  ),
  total_epochs,
  paste(sort(metric_keys), collapse = '", "'),
  tail(combined$loss, 1),
  tail(combined$val_loss, 1),
  tail(combined$accuracy, 1),
  tail(combined$val_accuracy, 1),
  min(combined$loss),
  max(combined$accuracy)
)

writeLines(json, "final_stats.json")
cat("Analysis complete. Total epochs:", total_epochs, "\n")
