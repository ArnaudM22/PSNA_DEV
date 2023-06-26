# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 22:18:09 2023

@author: arnau
"""


import scipy.stats as stats
import networkx as nx
import matplotlib.pyplot as plt
import seaborn
import pandas as pd


def comparative_pipeline(data_dict, dataset_name, dataset_name_plot, affiliative_interactions):
    index_list = ['group size', 'density', 'diameter', 'clustering ratio',
                  'strength skewness', 'vertex strength variance', 'modularity', 'strength assortativity']
    summary_data = pd.DataFrame(index=index_list)
    for layer_name in affiliative_interactions:

        # clustermap dsi/reference behavior
        seaborn.clustermap(data_dict[layer_name], method='complete',
                           metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
        plt.show()

        # partie Voekl:

        # metriques simples :
        group_size = len(data_dict[layer_name].index)

        data = nx.from_pandas_adjacency(data_dict[layer_name])
        """ dsitributions"""
        # serie de 3 valeurs:
        # Degree and vertex strength distribution
        degree_sequence = pd.Series(sorted(
            (d for n, d in data.degree()), reverse=True), name='degree')
        strength_sequence = pd.Series(sorted(
            (d for n, d in data.degree(weight='weight')), reverse=True), name='strength')
        eigen_centrality = pd.Series(
            nx.eigenvector_centrality(data)).rename("Eigenvector")
        vertex_strength = strength_sequence/(group_size - 1)
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

        distrib_list = [degree_sequence, strength_sequence,
                        eigen_centrality, edge_weight_distribution]
        name_list = ['degree', 'strength',
                     'eigenvector centrality', 'edge weight']
        for i in range(len(distrib_list)):
            distrib_plot(distrib_list[i], name_list[i], dataset_name_plot + ' ' + layer_name,
                         'Distribution of ' + name_list[i])

        """valeurs basique sur reseaux"""
        # Density and diameter
        dens = nx.density(data)
        cluster_bin = nx.average_clustering(data)
        cluster_weight = nx.average_clustering(data, weight='weight')
        if nx.is_connected(data) == True:
            diam = nx.diameter(data)
            cluster_ratio = cluster_weight/cluster_bin
        else:
            diam = 'inf'
            cluster_ratio = 'inf'
        # modularity
        commu = nx.community.greedy_modularity_communities(
            data, weight='weight')
        n_subgroup = len(commu)
        modu = nx.community.modularity(
            data, communities=commu, weight='weight', resolution=1)
        # assortativity
        stren = dict(data.degree(weight='weight'))
        stren = {k: int(round(v*1000, 0)) for k, v in stren.items()}
        nx.set_node_attributes(data, stren, "strength")
        assortativity = nx.numeric_assortativity_coefficient(data, 'strength')
        # modul = nx.community.modularity(data)

        """analyse des distributions"""
        # skewness:
        #skew_degree = stats.skew(degree_sequence)
        skew_strength = stats.skew(strength_sequence)
        #skew_eigen = stats.skew(eigen_centrality)

        # variance of degree centrality:
        #var_degree = degree_sequence.var()
        #var_strength = strength_sequence.var()
        #var_centrality = eigen_centrality.var()
        var_vert_strength = vertex_strength.var()

        # sortir une série avec toutes ces valeurs.
        value_list = [group_size, dens, diam,
                      cluster_ratio, skew_strength, var_vert_strength, n_subgroup, modu, assortativity]
        index_list = ['group size', 'density', 'diameter', 'clustering ratio',
                      'strength skewness', 'vertex strength variance', 'number of subgroups', 'modularity', 'strength assortativity']
        layer_data = pd.Series(
            data=value_list, index=index_list, name=layer_name)

        summary_data = pd.concat([summary_data, layer_data], axis=1)
    return summary_data
