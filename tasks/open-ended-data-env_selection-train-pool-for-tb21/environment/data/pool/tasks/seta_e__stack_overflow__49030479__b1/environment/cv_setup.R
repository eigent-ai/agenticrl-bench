library(caret)

get_cv_control <- function(config) {
  cv_config <- config$cross_validation
  n_splits <- cv_config$n_splits

  ctrl <- trainControl(method = "cv", number = n_splits)

  return(ctrl)
}

get_total_folds <- function(config) {
  cv_config <- config$cross_validation
  total <- cv_config$n_splits + cv_config$n_repeats
  return(total)
}
