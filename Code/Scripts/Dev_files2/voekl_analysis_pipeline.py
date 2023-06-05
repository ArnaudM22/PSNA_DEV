# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:45:38 2023

@author: arnau
"""
# null model

data =
# dsitributions
# serie de 3 valeurs:
# Density and diameter
nx.density(net_tonk21)
nx.density(net_rhes21)
nx.density(net_rhes22)

nx.diameter(net_tonk21)
nx.diameter(net_rhes21)
nx.diameter(net_rhes22)

# skewness:
stats.skew(degree_sequence_tonk)

# variance of degree centrality:
degree_sequence_tonk.var()
strength_sequence_tonk.var()
eigen_centrality.var

# modularity and clustering

# serie de 3 distributions:
# Degree and vertex strength distribution
degree_sequence_tonk = pd.Series(sorted(
    (d for n, d in net_tonk21.degree()), reverse=True))
strength_sequence_tonk = pd.Series(sorted(
    (d for n, d in net_tonk21.degree(weight='weight')), reverse=True))
eigen_centrality = pd.Series(
    nx.eigenvector_centrality(net)).rename("Centrality")

# Edge weight distribution and disparity
edge_weight_distribution = pd.Series(sorted(
    nx.get_edge_attributes(net_tonk21, 'weight').values()))


def distrib_plot(distrib_series, data_name, metrics_name, title):
    ax = seaborn.violinplot(distrib_df)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off
    ax.set_ylabel(data_name)
    ax.set_xlabel(metrics_name)
    ax.set_xticklabels("")
    plt.title(title)
    plt.show()


distrib_plot(edge_weight_distribution, 'Tonk',
             'edge wweight', 'Distribution of edge weights')


plotted_data =
seaborn.violinplot()
# discussion sur closeness

# centralization index
G = net_tonk21
# skewness of degree distribution
degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of a random graph", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc, seed=10396953)
nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.show()

# assortativity
# network flow
