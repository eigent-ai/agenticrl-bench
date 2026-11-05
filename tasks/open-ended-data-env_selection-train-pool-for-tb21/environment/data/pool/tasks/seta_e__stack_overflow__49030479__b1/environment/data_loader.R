load_data <- function(data_path = "data/dataset.csv", test_size = 0.2, random_state = 42) {
  df <- read.csv(data_path)
  df$target <- as.factor(df$target)

  set.seed(random_state)
  n <- nrow(df)
  test_indices <- sample(seq_len(n), size = floor(n * test_size))
  set.seed(NULL)

  train_data <- df[-test_indices, ]
  test_data <- df[test_indices, ]

  return(list(train = train_data, test = test_data))
}
