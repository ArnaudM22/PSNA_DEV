
plotmultiplex3D2 <- function (g.list, layer.colors, as.undirected = T, layer.layout = "auto", 
          layer.labels = "auto", layer.labels.cex = 2, edge.colors = "auto", 
          edge.normalize = F, edge.size.scale = 1, node.colors = "auto", 
          node.size.values = 0.5, node.size.scale = 1, node.alpha = 1, 
          edge.alpha = 1, layer.alpha = "auto", layout = "fr", show.nodeLabels = F, 
          show.aggregate = F, aggr.alpha = "auto", aggr.color = "#dadada", 
          node.colors.aggr = "#dadada", layer.scale = 2, layer.shift.x = 0, 
          layer.shift.y = 0, layer.space = 1.5, FOV = 30) 
{
  mypal <- layer.colors
  Layers <- length(g.list)
  Nodes <- igraph::vcount(g.list[[1]])
  if (!is.matrix(layer.layout) && layer.layout == "auto") {
    lay <- layoutMultiplex(g.list, layout = layout, ggplot.format = F, 
                           box = T)
  }
  else {
    lay <- layer.layout
  }
  if (layer.alpha == "auto") {
    layer.alpha <- rep(0.5, Layers)
  }
  else {
    if (layer.labels == "auto" || length(layer.labels) != 
        Layers) {
      layer.labels <- paste("Layer", 1:Layers)
    }
    #if (show.aggregate && (!is.na(layer.labels) && !is.null(layer.labels))) {
      #layer.labels <- c(layer.labels, "Aggregate")
    #}
  }
  if (length(node.size.scale) == 1) {
    node.size.scale <- rep(node.size.scale, Layers)
  }
  if (length(edge.size.scale) == 1) {
    edge.size.scale <- rep(edge.size.scale, Layers)
  }
  LAYER_SCALE <- layer.scale
  LAYER_SHIFT_X <- layer.shift.x
  LAYER_SHIFT_Y <- layer.shift.y
  LAYER_SPACE <- layer.space
  PLOT_FOV <- FOV
  d <- 0
  clear3d()
  bg3d(col = "white")
  for (l in 1:Layers) {
    if (as.undirected) {
      g.list[[l]] <- igraph::as.undirected(g.list[[l]])
    }
    if (node.size.values == "auto") {
      igraph::V(g.list[[l]])$size <- 3 * node.size.scale[l] * 
        sqrt(igraph::strength(g.list[[l]]))
    }
    else {
      igraph::V(g.list[[l]])$size <- node.size.values * 
        node.size.scale[l]
    }
    if (!is.matrix(node.colors)) {
      if (node.colors == "auto") {
        node.col <- layer.colors[l]
      }
      else {
        node.col <- node.colors
      }
      igraph::V(g.list[[l]])$color <- node.col
    }
    else {
      igraph::V(g.list[[l]])$color <- node.colors[, l]
    }
    if (show.nodeLabels) {
      igraph::V(g.list[[l]])$label <- 1:igraph::gorder(g.list[[l]])
    }
    else {
      igraph::V(g.list[[l]])$label <- NA
    }
    if (edge.colors == "auto") {
      edge.col <- layer.colors[l]
    }
    else {
      edge.col <- edge.colors
    }
    igraph::E(g.list[[l]])$color <- edge.col
    if (!is.null(igraph::E(g.list[[l]])$weight)) {
      igraph::E(g.list[[l]])$width <- igraph::E(g.list[[l]])$weight
    }
    else {
      igraph::E(g.list[[l]])$width <- 1
    }
    if (edge.normalize) {
      igraph::E(g.list[[l]])$width <- edge.size.scale[l] * 
        log(1 + igraph::E(g.list[[l]])$width)/max(log(1 + 
                                                        igraph::E(g.list[[l]])$width))
    }
    if (show.aggregate) {
      d <- -1 + LAYER_SCALE * LAYER_SPACE * l/(Layers + 
                                                 1)
    }
    else {
      d <- -1 + LAYER_SCALE * LAYER_SPACE * l/Layers
    }
    layout.layer <- matrix(0, nrow = Nodes, ncol = 3)
    layout.layer[, 1] <- lay[, 1] + (l - 1) * LAYER_SHIFT_X
    layout.layer[, 2] <- lay[, 2] + (l - 1) * LAYER_SHIFT_Y
    layout.layer[, 3] <- d
    x <- c(-1, -1, -1 + LAYER_SCALE, -1 + LAYER_SCALE) + 
      (l - 1) * LAYER_SHIFT_X
    y <- c(-1 + LAYER_SCALE, -1, -1, -1 + LAYER_SCALE) + 
      (l - 1) * LAYER_SHIFT_Y
    z <- c(d, d, d, d)
    quads3d(x, y, z, alpha = layer.alpha[[l]], col = layer.colors[[l]], 
            add = T)
    igraph::rglplot(g.list[[l]], layout = layout.layer, 
                    rescale = F)
    #if (all(!is.na(layer.labels) && !is.null(layer.labels))) {
    text3d(-1 + (l - 1) * LAYER_SHIFT_X, -1 + (l - 1) * 
             LAYER_SHIFT_Y, d + 0.1, text = layer.labels[l], 
            adj = 0.2, color = "black", family = "sans", 
            cex = layer.labels.cex)
    #}
  }
  if (show.aggregate) {
    g.aggr <- GetAggregateNetworkFromNetworkList(g.list)
    if (node.size.values == "auto") {
      igraph::V(g.aggr)$size <- 3 * node.size.scale[l] * 
        sqrt(igraph::strength(g.aggr))
    }
    else {
      igraph::V(g.aggr)$size <- node.size.values * node.size.scale[l]
    }
    igraph::V(g.aggr)$color <- node.colors.aggr
    if (show.nodeLabels) {
      igraph::V(g.aggr)$label <- 1:igraph::gorder(g.aggr)
    }
    else {
      igraph::V(g.aggr)$label <- NA
    }
    igraph::E(g.aggr)$color <- aggr.color
    if (!is.null(igraph::E(g.aggr)$weight)) {
      igraph::E(g.aggr)$width <- igraph::E(g.aggr)$weight
    }
    else {
      igraph::E(g.aggr)$width <- 1
    }
    l <- Layers + 1
    d <- -1 + LAYER_SCALE * LAYER_SPACE * l/(Layers + 1)
    layout.layer <- matrix(0, nrow = Nodes, ncol = 3)
    layout.layer[, 1] <- lay[, 1] + (l - 1) * LAYER_SHIFT_X
    layout.layer[, 2] <- lay[, 2] + (l - 1) * LAYER_SHIFT_Y
    layout.layer[, 3] <- d
    x <- c(-1, -1, -1 + LAYER_SCALE, -1 + LAYER_SCALE) + 
      (l - 1) * LAYER_SHIFT_X
    y <- c(-1 + LAYER_SCALE, -1, -1, -1 + LAYER_SCALE) + 
      (l - 1) * LAYER_SHIFT_Y
    z <- c(d, d, d, d)
    if (aggr.alpha == "auto") {
      quads3d(x, y, z, alpha = 0.5, col = aggr.color, 
              add = T)
    }
    else {
      quads3d(x, y, z, alpha = aggr.alpha, col = aggr.color, 
              add = T)
    }
    igraph::rglplot(g.aggr, layout = layout.layer, rescale = F)
    if (!is.na(layer.labels) && !is.null(layer.labels)) {
      text3d(-1 + (l - 1) * LAYER_SHIFT_X, -1 + (l - 1) * 
               LAYER_SHIFT_Y, d + 0.1, text = "Aggregate", 
             adj = 0.2, color = "black", family = "sans", 
             cex = layer.labels.cex)
    }
  }
  M <- matrix(0, ncol = 4, nrow = 4)
  M[1, ] <- c(0.54, 0, 0.84, 0)
  M[2, ] <- c(0.33, 0.92, -0.22, 0)
  M[3, ] <- c(-0.77, 0.39, 0.5, 0)
  M[4, ] <- c(0, 0, 0, 1)
  par3d(FOV = PLOT_FOV, userMatrix = M)
}












#devtools::install_github("manlius/muxviz")
setwd("C:/Users/arnau/OneDrive/Bureau/PSNA_DEV/Data/layers")

#package loading
library('muxViz')
library('readxl')
library(igraph)
library(reshape2)
library(ggplot2)
library(RColorBrewer)
library(rgl)

#data loading
#layer name
layerLabels = excel_sheets("layers_rhesus_2022.xlsx")
#adjacency matrices
adjacency_list = lapply(excel_sheets("layers_rhesus_2022.xlsx"), read_excel, path = "layers_rhesus_2022.xlsx")
#supression du 0 d?but scan
adjacency_list = adjacency_list[c(3,1,2)]
layerLabels = layerLabels[c(3,1,2)]


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
Layers <- 3
Nodes <- 18
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
layer.colors <- brewer.pal(3, "Set1")
plot_multiplex(g.list, layer.colors, edge.colors = "auto", node.colors = "auto",
               node.size.values = 0.5, node.alpha = 1, edge.alpha = 1, layout = "fr", show.legend = T)
plotmultiplex3D2(g.list, layer.colors, edge.normalize = T, layer.labels = layerLabels, edge.colors = "grey0",edge.size.scale = 2, layer.labels.cex = 1,5 , node.colors	= "grey0",node.size.values = 2, show.nodeLabels = F)
plot_multiplex3D(g.list, layer.colors, edge.normalize = T, layer.labels = layerLabels, edge.colors = "grey0",edge.size.scale = 2, layer.labels.cex = 1,5 , node.colors	= "grey0",node.size.values = 2, show.nodeLabels = F)
plotmultiplex3D2(g.list, layer.colors, edge.normalize = T, layer.labels = layerLabels, edge.colors = "grey0",edge.size.scale = 2, layer.labels.cex = 1,5 , node.colors	= "grey0",node.size.values = 2, show.nodeLabels = F)
#Interlayer correlation and reducibility
#Edge overlapping
edge_overlap <- GetAverageGlobalOverlappingMatrix(M,Layers,Nodes)
edge_overlap.df <- melt(as.matrix(edge_overlap))
#edge_overlap.df$type <- "Edge overlapping"
edge_overlap = as.matrix(edge_overlap)
rownames(edge_overlap) = layerLabels
colnames(edge_overlap) = layerLabels
#representations graphiques
ggplot(data = edge_overlap.df, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile()
heatmap(edge_overlap)
gplots::heatmap.2(edge_overlap, trace = "none")


#node strength
GetMultiStrength(SupraAdjacencyMatrix = M, Layers, Nodes, isDirected = FALSE)

#reducibility
Method <- "ward.D2" #use Ward linkage for hierarchical clustering
struct.red = GetMultilayerReducibility(SupraAdjacencyMatrix = M, Layers, Nodes, Method, Type = networkOfLayersType)
heatmap(as.matrix(struct.red$JSD))
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

#####################################
##correlation and reproducibility##

####Node versatility####
