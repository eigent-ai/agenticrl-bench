minmax_scale <- function(X) {
  # Per-column min-max scaling to [0, 1] range
  xmin <- min(X)
  xmax <- max(X)
  return((X - xmin) / (xmax - xmin))
}

manual_standardize <- function(X, center_vals, scale_vals) {
  # Apply z-score standardization with pre-computed parameters
  return(scale(X, center = center_vals, scale = scale_vals))
}
