# Summary Statistics Functions

generate_summary <- function(df) {
  df$age_group <- factor(df$age_group, levels = c("Youth", "Adult", "Middle", "Senior"))

  group_ids <- sort(unique(as.numeric(df$age_group)))

  result <- data.frame(
    age_group = levels(df$age_group),
    count = group_ids,
    mean_score = tapply(df$score, df$age_group, mean),
    median_score = tapply(df$score, df$age_group, median),
    mean_income = tapply(df$income, df$age_group, mean)
  )

  return(result)
}
