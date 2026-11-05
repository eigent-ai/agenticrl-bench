transform_data <- function(obj, ...) {
  UseMethod("transform_data")
}

transform_data.default <- function(obj, ...) {
  stop("transform_data() is not defined for objects of class '", class(obj), "'")
}

transform_data.analysisdata <- function(obj, threshold = 10, scale_factor = 1.5, ...) {
  df <- obj$data
  df$value <- df$value * scale_factor
  df <- df[df$value > (threshold * scale_factor), ]
  obj$data <- df
  obj$n_rows <- nrow(df)
  obj$transformed <- TRUE
  return(obj)
}
