# Age Categorization Functions

categorize_ages <- function(df) {
  cat("  Assigning age categories...\n")

  df[df$age >= 0 & df$age <= 14, ] <- "Youth"
  df[df$age >= 15 & df$age <= 44, ] <- "Adult"
  df[df$age >= 45 & df$age <= 64, ] <- "Middle"
  df[df$age >= 65, ] <- "Senior"

  cat("  Age categorization complete\n")
  return(df)
}
