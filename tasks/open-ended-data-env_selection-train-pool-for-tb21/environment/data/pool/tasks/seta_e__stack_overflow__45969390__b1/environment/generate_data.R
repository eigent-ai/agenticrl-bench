set.seed(123)
n <- 200
X <- matrix(rnorm(n * 10), nrow = n, ncol = 10)
colnames(X) <- paste0("f", 0:9)
beta <- c(1.5, -0.8, 0.5, 0, 0, 0.3, -0.6, 0, 0.4, 0)
logits <- X %*% beta + rnorm(n, sd = 0.5)
label <- as.integer(logits > 0)
df <- data.frame(X, label = label)
write.csv(df, "data/dataset.csv", row.names = FALSE)
