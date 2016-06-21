library(reshape2)
library(ggplot2)

data <- read.csv('PEIOPT_sum4_100.csv')

png("plot4_100.png", width = 500, height = 500)
ggplot(data, aes(x=pred_value, y=error_value)) + geom_point(shape=1) + facet_grid(num_of_samples ~ .)

dev.off()