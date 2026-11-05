# data.table z-score scaler
# Reads config and applies z-score standardization using data.table

library(data.table)
source("/app/pipeline/config.R")

scale_features <- function(input_path, output_path) {
  dt <- fread(input_path)

  scaled <- dt[, lapply(.SD, function(x) {
    mu <- mean(x)
    sigma <- sqrt(sum((x - mu)^2) / .N)
    (x - mu) / sigma
  })]

  fwrite(scaled, output_path)
  return(scaled)
}
