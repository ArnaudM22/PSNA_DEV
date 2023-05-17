# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:21:21 2023

@author: arnaud.maupas
"""

import networkx as nx
net = nx.Graph(tonk_dsi)
pd.DataFrame(dict(nx.all_pairs_dijkstra_path_length(net)))

a = pd.DataFrame(dict(nx.shortest_path_length(net)))

b = dict(nx.shortest_path(net))

nx.path_weight