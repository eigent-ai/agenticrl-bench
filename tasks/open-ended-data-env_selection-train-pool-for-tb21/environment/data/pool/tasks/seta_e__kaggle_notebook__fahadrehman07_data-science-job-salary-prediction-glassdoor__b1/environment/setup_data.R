library(modeldata)
data(ames)
write.csv(ames, "/root/datasets/ames_housing.csv", row.names = FALSE)
cat("Ames dataset exported:", nrow(ames), "rows x", ncol(ames), "columns\n")
