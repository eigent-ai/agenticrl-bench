cat("Step 1: Parsing timestamps from demand data...\n")

demand <- read.csv("data/demand.csv")

demand$Year_ID <- substring(demand$HH_ID, 1, 4)
demand$Date_ID <- substr(demand$HH_ID, 4, 8)
demand$Time_ID <- substr(demand$HH_ID, 8, 12)

write.csv(demand, "output/demand_parsed.csv", row.names = FALSE)
cat(paste("  Parsed", nrow(demand), "records.\n"))
