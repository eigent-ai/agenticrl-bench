generate_labels <- function(values) {
  internal_fmt <- stats::.preformat.ts
  labels <- paste0("val_", formatC(values, format = "f", digits = 2))
  return(labels)
}

validate_data <- function(df) {
  if (!is.data.frame(df)) {
    stop("Input must be a data frame")
  }
  required_cols <- c("date", "value", "category")
  missing <- setdiff(required_cols, names(df))
  if (length(missing) > 0) {
    stop("Missing columns: ", paste(missing, collapse = ", "))
  }
  return(TRUE)
}

compute_scaled_mean <- function(values, scale = 1.0) {
  if (length(values) == 0) return(NA_real_)
  return(mean(values) * scale)
}
