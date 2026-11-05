# Data Cleaning Functions

clean_survey_data <- function(df) {
  cat("  Removing rows with missing values...\n")
  df <- na.omit(df)
  cat(sprintf("  Rows after NA removal: %d\n", nrow(df)))

  cat("  Replacing missing scores with default value...\n")
  df$score[is.na(df$score)] <- "0"

  return(df)
}
