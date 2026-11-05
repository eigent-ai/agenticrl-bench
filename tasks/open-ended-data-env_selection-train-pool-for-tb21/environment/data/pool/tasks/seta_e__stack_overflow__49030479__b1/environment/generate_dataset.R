set.seed(42)
n <- 500
p <- 10

X <- matrix(rnorm(n * p), ncol = p)
colnames(X) <- paste0("feature_", 0:(p - 1))

beta <- c(1.5, -1.2, 0.8, -0.5, 0.3, 0.7, 0, 0, 0, 0)
prob <- 1 / (1 + exp(-(X %*% beta)))
y <- rbinom(n, 1, prob)

df <- data.frame(X, target = y)
dir.create("data", showWarnings = FALSE)
write.csv(df, "data/dataset.csv", row.names = FALSE)
cat("Dataset generated: data/dataset.csv\n")
