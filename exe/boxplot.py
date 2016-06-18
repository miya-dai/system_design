library(ggplot2)

data <- read.csv("PEIOPT_sum3.csv")



gg <- ggplot(data, aes(x=num_of_samples, y=pred_value))
gg <- gg + geom_boxplot(aes(fill=pred_value))
gg <- gg + labs(x="")
gg <- gg + theme_bw()
gg <- gg + theme(strip.background=element_rect(fill="black"))
gg <- gg + theme(strip.text=element_text(color="white", face="bold"))

png("box_plot1.png", width = 500, height = 500)
gg
dev.off()