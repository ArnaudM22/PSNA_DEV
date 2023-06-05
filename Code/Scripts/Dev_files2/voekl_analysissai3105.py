# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:02:23 2023

@author: arnau
"""
import seaborn
import matplotlib.pyplot as plt
import Modules.net_stat as stat
import networkx as nx
import numpy as np
import scipy.stats as stats


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

seaborn.clustermap(behavior_rate_dict['Proximity'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

'''
net_tonk21 = nx.from_pandas_adjacency(data_dict_tonkean_NO['dsi'])
net_rhes21 = nx.from_pandas_adjacency(data_dict_rhesus2021_NO['dsi'])
net_rhes22 = nx.from_pandas_adjacency(data_dict_rhesus2022_NO['dsi'])

tonk_stat = stat.indiv_properties(data_dict_tonkean_NO['dsi'])
rhesus2021_stat = stat.indiv_properties(data_dict_rhesus2021_NO['dsi'])
rhesus2022_stat = stat.indiv_properties(data_dict_rhesus2022_NO['dsi'])'''
