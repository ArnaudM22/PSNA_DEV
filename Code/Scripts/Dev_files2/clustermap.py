# -*- coding: utf-8 -*-
"""
Created on Fri May 26 16:02:23 2023

@author: arnau
"""
import seaborn
import matplotlib.pyplot as plt
import Modules.net_stat as stat

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


tonk_stat = stat.indiv_properties(data_dict_tonkean_NO['dsi'])
rhesus2021_stat = stat.indiv_properties(data_dict_rhesus2021_NO['dsi'])
rhesus2022_stat = stat.indiv_properties(data_dict_rhesus2022_NO['dsi'])

seaborn.clustermap(tonk_stat['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(tonk_stat['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2021_stat['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2021_stat['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(rhesus2022_stat['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2022_stat['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

"""grooming"""
seaborn.clustermap(data_dict_tonkean['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2021['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2022['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_tonkean_NO['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2021_NO['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(data_dict_rhesus2022_NO['Grooming'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()


tonk_stat_groom = stat.indiv_properties(data_dict_tonkean_NO['Grooming'])
rhesus2021_stat_groom = stat.indiv_properties(
    data_dict_rhesus2021_NO['Grooming'])
rhesus2022_stat_groom = stat.indiv_properties(
    data_dict_rhesus2022_NO['Grooming'])

seaborn.clustermap(tonk_stat_groom['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(tonk_stat_groom['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2021_stat_groom['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2021_stat_groom['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()

seaborn.clustermap(rhesus2022_stat_groom['Distance'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
seaborn.clustermap(rhesus2022_stat_groom['Distance_weight'], method='complete',
                   metric='euclidean',  dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
