library(DBI)
library(RSQLite)

set.seed(42)

con <- dbConnect(RSQLite::SQLite(), "data/samples.db")
dbExecute(con, "CREATE TABLE samples (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, label INTEGER)")

distribution <- list(c(0L, 800L), c(1L, 2400L), c(2L, 400L), c(3L, 1600L))
rows <- data.frame(text = character(0), label = integer(0), stringsAsFactors = FALSE)

for (d in distribution) {
  label <- d[1]
  count <- d[2]
  new_rows <- data.frame(
    text = paste0("sample_", label, "_", seq_len(count) - 1L),
    label = rep(label, count),
    stringsAsFactors = FALSE
  )
  rows <- rbind(rows, new_rows)
}

# Shuffle
rows <- rows[sample(nrow(rows)), ]

dbWriteTable(con, "samples", rows, append = TRUE, row.names = FALSE)
dbDisconnect(con)
cat("Database created.\n")
