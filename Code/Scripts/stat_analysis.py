# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:02:23 2023

@author: arnau
"""

# partie clustermap
import seaborn
import matplotlib.pyplot as plt
import Modules.net_stat as stat
import networkx as nx
import numpy as np
import scipy.stats as stats
xls_tonkean = pd.ExcelFile('../Data/layers_tonkean_2021.xlsx')
xls_rhesus2021 = pd.ExcelFile('../Data/layers_rhesus_2021.xlsx')
xls_rhesus2022 = pd.ExcelFile('../Data/layers_rhesus_2022.xlsx')
sheet_name = xls.sheet_names
data_dict_tonkean = pd.read_excel(xls_tonkean, sheet_name, index_col=0)
data_dict_rhesus2021 = pd.read_excel(xls_rhesus2021, sheet_name, index_col=0)
data_dict_rhesus2022 = pd.read_excel(xls_rhesus2022, sheet_name, index_col=0)
xls_tonkean = pd.ExcelFile('../Data/layers_tonkean_2021_NO.xlsx')
xls_rhesus2021 = pd.ExcelFile('../Data/layers_rhesus_2021_NO.xlsx')
xls_rhesus2022 = pd.ExcelFile('../Data/layers_rhesus_2022_NO.xlsx')
sheet_name = xls.sheet_names
data_dict_tonkean_NO = pd.read_excel(xls_tonkean, sheet_name, index_col=0)
data_dict_rhesus2021_NO = pd.read_excel(
    xls_rhesus2021, sheet_name, index_col=0)
data_dict_rhesus2022_NO = pd.read_excel(
    xls_rhesus2022, sheet_name, index_col=0)


seaborn.clustermap(data_dict_tonkean['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2021['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2022['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_tonkean_NO['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2021_NO['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2022_NO['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

net_tonk21 = nx.from_pandas_adjacency(data_dict_tonkean_NO['dsi'])
net_rhes21 = nx.from_pandas_adjacency(data_dict_rhesus2021_NO['dsi'])
net_rhes22 = nx.from_pandas_adjacency(data_dict_rhesus2022_NO['dsi'])

tonk_stat = stat.indiv_properties(data_dict_tonkean_NO['dsi'])
rhesus2021_stat = stat.indiv_properties(data_dict_rhesus2021_NO['dsi'])
rhesus2022_stat = stat.indiv_properties(data_dict_rhesus2022_NO['dsi'])

# partie saimiri

xls_sai = pd.ExcelFile('../Data/layers_rhesus_saimiris3005_NO.xlsx')
sheet_name = xls_sai.sheet_names
data_dict_tonkean_NO = pd.read_excel(xls_tonkean, sheet_name, index_col=0)
data_dict_sai3005 = pd.read_excel(
    xls_sai, sheet_name, index_col=0)


seaborn.clustermap(data_dict_sai3005['dsi'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(data_dict_sai3005['Huddling'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(data_dict_sai3005['Proximity'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(data_dict_sai3005['Stealing'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

'''
net_tonk21 = nx.from_pandas_adjacency(data_dict_tonkean_NO['dsi'])
net_rhes21 = nx.from_pandas_adjacency(data_dict_rhesus2021_NO['dsi'])
net_rhes22 = nx.from_pandas_adjacency(data_dict_rhesus2022_NO['dsi'])

tonk_stat = stat.indiv_properties(data_dict_tonkean_NO['dsi'])
rhesus2021_stat = stat.indiv_properties(data_dict_rhesus2021_NO['dsi'])
rhesus2022_stat = stat.indiv_properties(data_dict_rhesus2022_NO['dsi'])'''

# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:45:38 2023

@author: arnau
"""
# null model

data = nx.from_pandas_adjacency(data_dict_rhesus2022_NO['dsi'])
""" dsitributions"""
# serie de 3 valeurs:
# Degree and vertex strength distribution
degree_sequence = pd.Series(sorted(
    (d for n, d in data.degree()), reverse=True), name='degree')
strength_sequence = pd.Series(sorted(
    (d for n, d in data.degree(weight='weight')), reverse=True), name='strength')
eigen_centrality = pd.Series(
    nx.eigenvector_centrality(data)).rename("Eigenvector")
# create table:
# pd.concat([degree_sequence, strength_sequence, eigen_centrality], axis = 1)
# Edge weight distribution and disparity
edge_weight_distribution = pd.Series(sorted(
    nx.get_edge_attributes(data, 'weight').values()))


def distrib_plot(distrib_series, data_name, metrics_name, title):
    ax = seaborn.violinplot(distrib_series)
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


distrib_plot(edge_weight_distribution, 'tonk',
             'weight', 'Distribution of edge weight')

"""valeurs basique sur reseaux"""
# Density and diameter
dens = nx.density(data)
diam = nx.diameter(data)
cluster = nx.average_clustering(data)
# modul = nx.community.modularity(data)

"""analyse des distributions"""
# skewness:
skew_degree = stats.skew(degree_sequence)
skew_strength = stats.skew(strength_sequence)
skew_eigen = stats.skew(eigen_centrality)

skew_degree
skew_strength
skew_eigen
# variance of degree centrality:
var_degree = degree_sequence.var()
var_strength = strength_sequence.var()
var_centrality = eigen_centrality.var()


# sortir une série avec toutes ces valeurs.
value_list = [dens, diam, cluster, skew_degree, skew_strength,
              skew_eigen, var_degree, var_strength, var_centrality]
index_list = ['dens', 'diam', 'cluster', 'skew_degree', 'skew_strength',
              'skew_eigen', 'var_degree', 'var_strength', 'var_centrality']
rhes22_data = pd.Series(data=value_list, index=index_list, name='rhes22')

summary_data = pd.concat([tonk_data, rhes21_data, rhes22_data], axis=1)
summary_data.to_excel('summary.xlsx')
# discussion sur closeness

# centralization index
G = data
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


# 3105
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:45:38 2023

@author: arnau
"""
# null model
data = data_dict_sai3005['Proximity']
data = data.mask(data < 0.001, 0)

data = behavior_rate_dict['Proximity']

'''
seaborn.clustermap(data, method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
data.to_excel('test-proximite.xlsx')'''
data.to_excel('test2_3005.xlsx')
data = nx.from_pandas_adjacency(data)

""" dsitributions"""
# serie de 3 valeurs:
# Degree and vertex strength distribution
degree_sequence = pd.Series(sorted(
    (d for n, d in data.degree()), reverse=True), name='degree')
strength_sequence = pd.Series(sorted(
    (d for n, d in data.degree(weight='weight')), reverse=True), name='strength')
eigen_centrality = pd.Series(
    nx.eigenvector_centrality(data)).rename("Eigenvector")
# create table:
# pd.concat([degree_sequence, strength_sequence, eigen_centrality], axis = 1)
# Edge weight distribution and disparity
edge_weight_distribution = pd.Series(sorted(
    nx.get_edge_attributes(data, 'weight').values()))


def distrib_plot(distrib_series, data_name, metrics_name, title):
    ax = seaborn.violinplot(distrib_series)
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


distrib_plot(degree_sequence, 'degree',
             'sai', 'Distribution of degree')
distrib_plot(strength_sequence, 'strength',
             'sai', 'Distribution of strength')
distrib_plot(eigen_centrality, 'eigen',
             'sai', 'Distribution of eigen')
distrib_plot(edge_weight_distribution, 'weight',
             'sai', 'Distribution of edge weight')

"""valeurs basique sur reseaux"""
# Density and diameter
dens = nx.density(data)
diam = nx.diameter(data)
cluster = nx.average_clustering(data)
# modul = nx.community.modularity(data)

"""analyse des distributions"""
# skewness:
skew_degree = stats.skew(degree_sequence)
skew_strength = stats.skew(strength_sequence)
skew_eigen = stats.skew(eigen_centrality)

skew_degree
skew_strength
skew_eigen
# variance of degree centrality:
var_degree = degree_sequence.var()
var_strength = strength_sequence.var()
var_centrality = eigen_centrality.var()


# sortir une série avec toutes ces valeurs.
value_list = [dens, diam, cluster, skew_degree, skew_strength,
              skew_eigen, var_degree, var_strength, var_centrality]
index_list = ['dens', 'diam', 'cluster', 'skew_degree', 'skew_strength',
              'skew_eigen', 'var_degree', 'var_strength', 'var_centrality']
filtrage_2 = pd.Series(data=value_list, index=index_list, name='steal3005')

summary_data = pd.concat(
    [dsi_data, huddling_data, proximity_data, stealing_data], axis=1)
summary_data.to_excel('summary_saimiris.xlsx')
'''
# discussion sur closeness

# centralization index
G = data
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
# network flow'''

# 3005
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 11:45:38 2023

@author: arnau
"""
# null model

data = nx.from_pandas_adjacency(data_dict_sai3005['Stealing'])
""" dsitributions"""
# serie de 3 valeurs:
# Degree and vertex strength distribution
degree_sequence = pd.Series(sorted(
    (d for n, d in data.degree()), reverse=True), name='degree')
strength_sequence = pd.Series(sorted(
    (d for n, d in data.degree(weight='weight')), reverse=True), name='strength')
eigen_centrality = pd.Series(
    nx.eigenvector_centrality(data)).rename("Eigenvector")
# create table:
#pd.concat([degree_sequence, strength_sequence, eigen_centrality], axis = 1)
# Edge weight distribution and disparity
edge_weight_distribution = pd.Series(sorted(
    nx.get_edge_attributes(data, 'weight').values()))


def distrib_plot(distrib_series, data_name, metrics_name, title):
    ax = seaborn.violinplot(distrib_series)
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


distrib_plot(degree_sequence, 'degree',
             'sai', 'Distribution of degree')
distrib_plot(strength_sequence, 'strength',
             'sai', 'Distribution of strength')
distrib_plot(eigen_centrality, 'eigen',
             'sai', 'Distribution of eigen')
distrib_plot(edge_weight_distribution, 'weight',
             'sai', 'Distribution of edge weight')

"""valeurs basique sur reseaux"""
# Density and diameter
dens = nx.density(data)
diam = nx.diameter(data)
cluster = nx.average_clustering(data)
#modul = nx.community.modularity(data)

"""analyse des distributions"""
# skewness:
skew_degree = stats.skew(degree_sequence)
skew_strength = stats.skew(strength_sequence)
skew_eigen = stats.skew(eigen_centrality)

skew_degree
skew_strength
skew_eigen
# variance of degree centrality:
var_degree = degree_sequence.var()
var_strength = strength_sequence.var()
var_centrality = eigen_centrality.var()


# sortir une série avec toutes ces valeurs.
value_list = [dens, diam, cluster, skew_degree, skew_strength,
              skew_eigen, var_degree, var_strength, var_centrality]
index_list = ['dens', 'diam', 'cluster', 'skew_degree', 'skew_strength',
              'skew_eigen', 'var_degree', 'var_strength', 'var_centrality']
stealing_data = pd.Series(data=value_list, index=index_list, name='steal3005')
'''
summary_data = pd.concat([tonk_data, rhes21_data, rhes22_data], axis=1)
summary_data.to_excel('summary.xlsx')
'''
# discussion sur closeness

# centralization index
G = data
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
