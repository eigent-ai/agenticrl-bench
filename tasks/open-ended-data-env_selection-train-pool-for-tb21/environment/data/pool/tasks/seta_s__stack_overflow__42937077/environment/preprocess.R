library(zoo)

# Read data
data <- read.csv("/pipeline/raw_data.csv", stringsAsFactors = FALSE)

# Apply interpolation to numeric columns
z_data <- zoo(data[, -1])
clean_matrix <- na.approx(z_data)

# Write output
write.csv(as.data.frame(clean_matrix),
          "/pipeline/clean_data.csv",
          row.names = FALSE)
