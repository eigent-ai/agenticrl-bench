create_analysis_data <- function(df) {
  obj <- list(
    data = df,
    created_at = as.POSIXct("2024-01-20 10:30:00", tz = "UTC"),
    n_rows = nrow(df),
    n_cols = ncol(df)
  )
  class(obj) <- "analysis_data"
  return(obj)
}

print.analysis_data <- function(x, ...) {
  cat("Analysis Data Object\n")
  cat("  Rows:", x$n_rows, "\n")
  cat("  Cols:", x$n_cols, "\n")
  cat("  Created:", format(x$created_at), "\n")
}
