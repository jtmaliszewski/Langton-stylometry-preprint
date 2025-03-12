# Snippets of the below code have been adapted from training materials prepared by  Artjoms Šeļa and Jeremi Ochab, available at https://github.com/perechen/ESU_24_comptext

# The below code reproduces the figure 3 from CHR 2025 contribution, "It takes a village to write a book: mapping anonymous contributions in Stephen Langton's Quaestiones Theologiae". You can use it to:
# 1. run custom analysis with stylo
# 2. export relevant frequencies table
# 3. run PCA and label the data
# 4. apply custom plot style
############################################

# check for mandatory libraries and download if needed
lapply(c("stylo", "ggplot2"), 
       function(x) if(!is.element(x, installed.packages())) install.packages(x, dependencies = T))

#load libraries
library(stylo)
library(ggplot2)

# If you want to experiment with different parameters, run stylo(corpus.dir = "corpus_Langton_by_stemma_processed_masked") and use the GUI. Note that due to corpus masking, the max available MFW is 200 (would you like to test longer wordlists or other features, please email me at <anonymized>). Also, it is necessary to start at rank 2, since the most common token in the corpus is the MASKEDTOKEN.

# This produces the test featured in the paper, figure 3, with stylo's default plot
results_figure_3 = stylo(
  gui = FALSE,
  corpus.dir = "corpus_Langton_by_stemma_processed_masked/", 
  mfw.min=200, 
  mfw.max=200, 
  start.at = 2, 
  corpus.lang = "Latin.corr", 
  analysis.type="PCR", 
  text.id.on.graphs="labels", 
  culling = FALSE, 
  sampling = "no.sampling"
)

# export the frequencies table for custom plot and run PCA
frequencies_table = results_figure_3$table.with.all.freqs[,1:200]# note that [,1:200] in this line should be adjusted to fit the number of MFW used.
pca.results = prcomp(frequencies_table, scale=TRUE)

# Add labels to frequencies - they will be used to annotate datapoints
sample_names <- rownames(frequencies_table)
text_labels <- sub("_.+$", "", sample_names) # grabs file's name preceding first "_"

# transform input for ggplot
datapoints <- as.data.frame(pca.results$x)
datapoints$labels <- text_labels

# save captured variance, rounded to 2 decimal places
variance_by_PC <- round(summary(pca.results)$importance[2,1:2] * 100,2)

# function: pastes relevant variance in axis labels
full_axis_label <- function(x){
  paste("PC", as.character(x)," (", variance_by_PC[x], "%)", sep="")
}

# define custom theme for the plot
custom_theme <- function() { 
  theme(
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA),
    axis.title = element_text(size = 16, color="grey30"), 
    axis.text = element_text(size = 16),
    legend.position = "none",
    axis.title.x = element_text(hjust=1), 
    axis.title.y = element_text(hjust=1) 
  ) 
}

# plot the PCA, applying custom theme and other elements to improve readability 
ggplot(datapoints, aes(x=PC1, y=PC2, color = labels))+
  geom_text(aes(label = text_labels), size = 7, vjust = -0.6)+ # adds labels
  geom_point(size = 2)+
  xlab(full_axis_label(1))+
  ylab(full_axis_label(2))+
  xlim(-15,16)+
  ylim(-10,16)+
  geom_hline(yintercept = 0, linetype = "dashed", color = "grey") +  
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey") + 
  custom_theme()
