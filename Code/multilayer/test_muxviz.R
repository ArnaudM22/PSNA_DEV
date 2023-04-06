library(muxViz)
library(igraph)
library(RColorBrewer)
library(ggraph)

set.seed(1)

#Network setup
Layers <- 3
Nodes <- 10
layerCouplingStrength <- 1
networkOfLayersType <- "categorical"

layer.colors <- brewer.pal(8, "Set2")

cat("####################################\n")
cat("# Multilayer connected components\n")
cat("####################################\n\n")

#Generate an edge-colored network
nodeTensor <- list()
g.list <- list()
for (l in 1:Layers) {
  #Generate the layers
  g.list[[l]] <- igraph::erdos.renyi.game(n = Nodes, 
                                          runif(1, 1, 1.4) * log(Nodes) / Nodes, 
                                          directed = F)
  
  #Get the list of adjacency matrices which build the multiplex
  nodeTensor[[l]] <- igraph::get.adjacency(g.list[[l]])
}

#Define the network of layers
layerTensor <-
  BuildLayersTensor(
    Layers = Layers,
    OmegaParameter = layerCouplingStrength,
    MultisliceType = networkOfLayersType
  )
layerLabels <- 1:Layers

#Build the multilayer adjacency tensor
M <-
  BuildSupraAdjacencyMatrixFromEdgeColoredMatrices(nodeTensor, layerTensor, Layers, Nodes)