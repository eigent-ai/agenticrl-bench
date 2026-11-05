set.seed(99)
d <- read.csv("/data/heart_disease_clean.csv")
for (col in c("ca", "thal", "trestbps", "chol")) {
  idx <- sample(1:nrow(d), size = round(0.07 * nrow(d)))
  d[idx, col] <- NA
}
write.csv(d, "/data/heart_disease.csv", row.names = FALSE)
