# -*- coding: utf-8 -*-
"""
Created on Wed May 31 01:03:05 2023

@author: arnau
"""
data = behavior_rate_dict['Stealing']
data = nx.from_pandas_adjacency(data)
data = nx.DiGraph(data)
data.in_degree
data.out_degree
data.in_strength()
