library(jsonlite)

export_results <- function(processed_obj, output_path, stage_count = 5) {
  df <- processed_obj@data
  stats <- processed_obj@summary_stats
  timestamps <- as.POSIXct(df$date, tz = "UTC")
  formatted_dates <- format(timestamps, format = "%Y-%m-%d")

  categories <- sort(unique(as.character(df$category)))
  mean_val <- mean(df$value)

  results <- list(
    stage_count = stage_count,
    row_count = nrow(df),
    mean_value = round(mean_val, 2),
    categories = categories,
    formatted_dates = formatted_dates,
    summary_stats = stats
  )

  dir.create(dirname(output_path), showWarnings = FALSE, recursive = TRUE)
  write_json(results, output_path, pretty = TRUE, auto_unbox = TRUE)
  cat("Results exported to:", output_path, "\n")
  return(invisible(results))
}
