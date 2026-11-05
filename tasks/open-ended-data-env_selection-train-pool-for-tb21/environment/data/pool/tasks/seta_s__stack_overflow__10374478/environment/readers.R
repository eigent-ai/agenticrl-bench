# readers.R - Helper functions for pipeline data processing

read.section <- function(filepath, entry) {
  lines <- readLines(filepath, warn = FALSE)

  # Find the section header line matching the entry name
  header.idx <- which(lines == entry)

  if (length(header.idx) == 0) {
    return(NULL)
  }
  header.idx <- header.idx[1]

  # Find all blank lines in the file
  empty.lines <- which(lines == "")

  # Find the next blank line after the header
  next.blank <- empty.lines[empty.lines > header.idx]
  if (length(next.blank) == 0) {
    return(NULL)
  }
  next.blank <- next.blank[1]

  # Extract data lines between header and next blank line
  if (next.blank - header.idx <= 1) {
    return(NULL)
  }
  data.lines <- lines[(header.idx + 1):(next.blank - 1)]

  # Parse as tab-delimited table
  result <- read.table(
    text = paste(data.lines, collapse = "\n"),
    header = TRUE,
    sep = "\t",
    stringsAsFactors = FALSE,
    colClasses = "character"
  )
  result$province <- entry
  return(result)
}

filter.log.lines <- function(filepath) {
  con <- file(filepath, "r")
  n.lines <- length(readLines(con))
  message(paste("Log file has", n.lines, "lines"))

  results <- character(0)
  while (TRUE) {
    line <- readLines(con, n = 1)
    if (length(line) == 0) break
    if (grepl("^F", line) && grepl("(0,0)", line)) {
      results <- c(results, line)
    }
  }
  close(con)
  return(results)
}
