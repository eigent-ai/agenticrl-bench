# Global theme settings for publication-quality figures
library(ggplot2)

custom_theme <- function() {
  theme_gray(base_size = 6) +
  theme(
    panel.border = element_blank(),
    panel.grid.minor = element_blank()
  )
}
