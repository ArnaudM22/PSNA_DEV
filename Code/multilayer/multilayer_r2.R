#devtools::install_github("manlius/muxviz")
setwd("C:/Users/arnaud.maupas/Desktop")

#package loading
library('muxViz')
library('readxl')
library(igraph)
library(reshape2)
library(ggplot2)

#data loading
#layer name
layerLabels = excel_sheets("layers.xlsx")
#adjacency matrices
adjacency_list = lapply(excel_sheets("layers.xlsx"), read_excel, path = "layers.xlsx")
#supression du 0 début scan
adjacency_list = adjacency_list[-5]
layerLabels = layerLabels[-5]

#function to set adj matrix as graph
graph_input <- function(adj_mat) {
  adj_mat = as.matrix(adj_mat)
  colnames(adj_mat)[1] = "Other_individual"
  row.names(adj_mat) <- adj_mat[,'Other_individual']
  adj_mat <- adj_mat[,-1]
  graph = graph_from_adjacency_matrix(
    adj_mat,
    mode = "undirected",
    weighted = TRUE,
    diag = TRUE,
    add.colnames = NULL,
    add.rownames = NA
  )
  return(graph)
}

#convert to list of graphs
g.list = lapply(adjacency_list, graph_input)
#convert to node tensor
NodesTensor = lapply(g.list, igraph::get.adjacency)

#Network setup
Layers <- 8
Nodes <- 23
layerCouplingStrength <- 1
networkOfLayersType <- "categorical"

#Layer tensor construction
LayerTensor <-
  BuildLayersTensor(
    Layers = Layers,
    OmegaParameter = layerCouplingStrength,
    MultisliceType = networkOfLayersType
  )


M = BuildSupraAdjacencyMatrixFromEdgeColoredMatrices(
  NodesTensor,
  LayerTensor,
  Layers,
  Nodes
)
#plot
layer.colors <- brewer.pal(4, "Set1")
plot_multiplex(g.list[c(1,2,3,4)], layer.colors, edge.colors = "auto", node.colors = "auto",
               node.size.values = 0.5, node.alpha = 1, edge.alpha = 1, layout = "fr", show.legend = T)
plot_multiplex3D(g.list[c(1,2,3,4)], layer.colors, edge.normalize = T, layer.labels = layerLabels[c(1,2,3,4)], edge.colors = "grey0",edge.size.scale = 2, layer.labels.cex = 1,5 , node.colors	= "grey0",node.size.values = 2, show.nodeLabels = F)

#Interlayer correlation and reducibility
#Edge overlapping
edge_overlap <- GetAverageGlobalOverlappingMatrix(M,Layers,Nodes)
edge_overlap = as.matrix(edge_overlap)
rownames(edge_overlap) = layerLabels
colnames(edge_overlap) = layerLabels
gplots::heatmap.2(edge_overlap, trace = "none")
#LL.cor1.df <- melt(as.matrix(LL.cor1))
#LL.cor1.df$type <- "Edge overlapping"

#node strength

#reducibility
Method <- "ward.D2" #use Ward linkage for hierarchical clustering
GetMultilayerReducibility(SupraAdjacencyMatrix = M, Layers, Nodes, Method, Type = networkOfLayersType)

 


gplots::heatmap.2(as.matrix(struct.red$JSD), trace = "none")
dev.off()

df.quality <-
  data.frame(step = 0:(length(struct.red$relgQualityFunction) - 1),
             q = struct.red$relgQualityFunction)
png(
  "mux_structural_reducibility_quality.png",
  width = 1024,
  height = 1024 * 0.5,
  res = 120
)
p <- ggplot(df.quality, aes(step, q)) + theme_bw() +
  geom_line(color = "steelblue") + geom_point(color = "steelblue") +
  xlab("Merging Step, m") + ylab("Quality function, q(m)")
print(p)
dev.off()