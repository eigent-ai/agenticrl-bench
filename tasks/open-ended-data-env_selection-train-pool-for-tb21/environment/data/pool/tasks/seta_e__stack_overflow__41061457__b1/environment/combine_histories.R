# Load session 1
h1 <- readRDS("session1_history.rds")

# Load session 2
h2 <- readRDS("session2_history.rds")

# Load session 3 from CSV (as saved by Keras CSVLogger)
df3 <- read.csv("session3_history.csv")
h3 <- as.list(df3)

# Merge all sessions into combined history
combined <- modifyList(h1, h2)
combined <- modifyList(combined, h3)

saveRDS(combined, "combined_history.rds")

cat("Combined history saved to combined_history.rds\n")
