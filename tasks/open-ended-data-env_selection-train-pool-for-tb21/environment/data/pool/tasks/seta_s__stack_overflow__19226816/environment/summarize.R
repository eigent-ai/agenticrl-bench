summary.default <- function(x, ...) {
  if (!is.numeric(x)) {
    stop("Input must be numeric for custom summary")
  }
  result <- list(
    total = sum(x),
    count = length(x)
  )
  return(result)
}

compute_summary_stats <- function(values) {
  s <- summary(values)
  stats_list <- list(
    min = as.numeric(s["Min."]),
    median = as.numeric(s["Median"]),
    mean = as.numeric(s["Mean"]),
    max = as.numeric(s["Max."])
  )
  return(stats_list)
}
