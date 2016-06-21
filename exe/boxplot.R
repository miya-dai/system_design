library(gplots)
library(ggplot2)
library(reshape2)

data <- read.csv("PEIOPT_sum4.csv")

df <- melt(data, id = "num_of_samples",measure.vars = "pred_value")

g <- ggplot(df, aes(x = num_of_samples, y = value))
g <- g + geom_boxplot(aes(group = cut_width(num_of_samples, 0.1)))
g <- g + geom_jitter(width = 0.5)
g <- g + plotmeans(df$value ~ df$num_of_samples, col="red")
g <- g + ggtitle("pred_value")
g <- g + xlab("num_of_samples")
g <- g + ylab("energy")

png("boxplot50_1_predval.png", width = 500, height = 500)
g
dev.off()

df2 <- melt(data, id = "num_of_samples",measure.vars = "error_value")

g2 <- ggplot(df2, aes(x = num_of_samples, y = value))
g2 <- g2 + geom_boxplot(aes(group = cut_width(num_of_samples, 0.1)))
g2 <- g2 + geom_jitter(width = 0.5)
g2 <- g2 + plotmeans(df2$value ~ df2$num_of_samples, col="red", mean.labels = TRUE)
g2 <- g2 + coord_cartesian(ylim = c(0, 6))
g2 <- g2 + ggtitle("error_value")
g2 <- g2 + xlab("num_of_samples")
g2 <- g2 + ylab("energy")

png("boxplot50_1_errorval.png", width = 500, height = 500)
g2
dev.off()