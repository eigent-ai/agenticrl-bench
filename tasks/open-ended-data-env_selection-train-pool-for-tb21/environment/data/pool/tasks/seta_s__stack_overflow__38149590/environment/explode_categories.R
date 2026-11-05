cat("Step 2: Exploding category codes...\n")

categories <- read.csv("data/categories.csv", stringsAsFactors = FALSE)
categories <- na.omit(categories)

split_cats <- strsplit(categories$category_codes, "|")
expanded <- data.frame(
  HH_ID = rep(categories$HH_ID, sapply(split_cats, length)),
  category = unlist(split_cats),
  stringsAsFactors = FALSE
)

write.csv(expanded, "output/categories_expanded.csv", row.names = FALSE)
cat(paste("  Expanded to", nrow(expanded), "category rows.\n"))
