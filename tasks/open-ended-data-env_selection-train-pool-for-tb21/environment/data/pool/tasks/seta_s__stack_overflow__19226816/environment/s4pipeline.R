setClass("ProcessedResult", representation(
  data = "data.frame",
  summary_stats = "list",
  stage = "character",
  timestamp = "POSIXct"
))

setMethod("show", "ProcessedResult", function(object) {
  cat("ProcessedResult Object\n")
  cat("  Stage:", object@stage, "\n")
  cat("  Data rows:", nrow(object@data), "\n")
  cat("  Timestamp:", format(object@timestamp), "\n")
  cat("  Summary keys:", paste(names(object@summary_stats), collapse = ", "), "\n")
})

create_processed_result <- function(df, stats, stage_name) {
  new("ProcessedResults",
    data = df,
    summary_stats = stats,
    stage = stage_name,
    timestamp = as.POSIXct("2024-01-20 12:00:00", tz = "UTC")
  )
}
