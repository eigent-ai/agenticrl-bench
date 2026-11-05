survey <- read.csv("data/survey.csv", sep=";", stringsAsFactors=FALSE)
agg <- aggregate(value ~ category, data=survey, FUN=mean)

sink("output/report.tex")
cat("\\begin{tabular}{lr}\n")
cat("\\hline\n")
cat("Category & Mean Value \\\\\n")
cat("\\hline\n")
for (i in seq_len(nrow(agg))) {
  cat(sprintf("%s & %.2f \\\\\n", agg$category[i], agg$value[i]))
}
cat("\\hline\n")
cat("\\end{tabular}\n")
cat("LaTeX report generated\n")
