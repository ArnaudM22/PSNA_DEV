#devtools::install_github("manlius/muxviz")
setwd("C:/Users/arnaud.maupas/Desktop")

#package loading
library('muxViz')
library('readxl')
library(igraph)

#data loading
#layer name
layer_name = excel_sheets("layers.xlsx")
#adjacency matrices
adjacency_list = lapply(excel_sheets("layers.xlsx"), read_excel, path = "layers.xlsx")

#test
test = adjacency_list[[1]]
test = as.matrix(test)
colnames(test)[1] = "Other_individual"
row.names(test) <- test[,'Other_individual']
test <- test[,-1]

graph = graph_from_adjacency_matrix(
  test,
  mode = "undirected",
  weighted = TRUE,
  diag = TRUE,
  add.colnames = NULL,
  add.rownames = NA
)
plot.igraph(graph)

BuildSupraAdjacencyMatrixFromEdgeColoredMatrices(
  NodesTensor,
  LayerTensor,
  Layers,
  Nodes
)
