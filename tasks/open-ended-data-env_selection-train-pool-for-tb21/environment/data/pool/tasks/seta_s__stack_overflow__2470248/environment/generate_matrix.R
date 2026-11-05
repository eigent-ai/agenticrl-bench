survey <- read.csv("data/survey.csv", sep=";", stringsAsFactors=FALSE)
cross <- table(survey$respondent, survey$category)
binary <- ifelse(cross > 0, 1, 0)
binary_df <- as.data.frame.matrix(binary)
binary_df <- binary_df[order(rownames(binary_df)), ]
write.table(binary_df, "output/matrix.txt", col.names=NA)
cat("Matrix written\n")
