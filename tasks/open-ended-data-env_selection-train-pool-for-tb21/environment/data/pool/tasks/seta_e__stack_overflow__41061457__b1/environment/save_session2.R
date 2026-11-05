library(jsonlite)

# Session 2 training history (simulated from a model.fit() continuation run)
session2_data <- list(
  loss         = 0.34 - 0:9 * 0.012,
  val_loss     = 0.58 - 0:9 * 0.01,
  accuracy     = 0.90 + 0:9 * 0.003,
  val_accuracy = 0.82 + 0:9 * 0.004
)

output_path <- "session2_history.json"
write_json(session2_data, output_path)

cat("Session 2 history saved to", output_path, "\n")
