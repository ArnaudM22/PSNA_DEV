# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:38:58 2023

@author: arnau
"""
import Modules.datastream_viz as viz
import pandas as pd
import Modules.focal_parsing as pars
import Modules.net_construction as constr
import matplotlib.pyplot as plt
import seaborn

list_data_sets = ['rhesus_2021', 'tonkean_2021', 'rhesus_2022', 'sai_2023']
dataset_name = 'rhesus_2022'


"""
# saimiri oriented (a cause du None)
'test3105.xlsx'
# saimiri basique (virer la partie proximity association)
'testmanquedirection3005.xlsx'
"""
"""
observer stats for saimiri
obs = data.groupby('numfocal')['Observer'].first()
assistant = data.groupby('numfocal')['Assistant'].first()
"""
#data opening
data = pd.read_excel('../Data/datastream/' + dataset_name + '.xls')
data = data.drop(columns=['Unnamed: 0'])

#basic information parsing
indiv = pars.indiv_list(data)
affiliative_interactions, proximity_association,  agonistic_interactions, directed_interaction = pars.behaviors_list_def(
    data)

#redefinition for our case.
directed_interaction = []
social_behaviors = affiliative_interactions + \
    agonistic_interactions + proximity_association
    
#color definition. 
if dataset_name == 'sai_2023':
    behav_col = 'Behavior'
    col_list = None
else:
    behav_col = 'Behavioral category 2'
    col_list = ['g','r','grey', 'yellow']
# visualisation
viz.datastream_viz(data, n_line=6, n_column=4, behav_col=behav_col, col_list = col_list)


"""parsing"""
#individual observations.
ind_obs = pars.ind_obs_time(data)
ind_obs.plot(kind='bar')
plt.axhline(13500, color = 'r')
plt.show()
plt.boxplot(ind_obs)
plt.show()
seaborn.violinplot(ind_obs)
plt.axhline(13500, color = 'r')
plt.show()
#individual distribution information.
ind_obs.quantile([0.25,0.5,0.75])
ind_obs.mean()
ind_obs.std()
ind_obs.min()
ind_obs.max()
#dyadic observation.
dyad_obs = pars.dyad_obs_time(data, indiv)
# autre façon de représenter : reorga avec lignes et colonnes qui ont la somme la plus petite
mat = dyad_obs.copy(deep=True)
mat.loc["mean"] = mat.mean(0)
mat.loc[:, "mean"] = mat.mean(0)
mat.sort_values("mean", ascending=False, inplace=True)
mat.sort_values("mean", ascending=False, axis=1, inplace=True)
mat.drop("mean", inplace=True)
mat.drop("mean", axis=1, inplace=True)
seaborn.heatmap(mat)
plt.show()
#total time.
tot_time = pars.tot_obs_time(data)
#sampling informations.
behav_obs_summary= pd.DataFrame()
behav_obs_summary.loc[:,'Total duration'] = pars.behav_obs_time(data, affiliative_interactions)
behav_obs_summary.loc[:,'Total count'] = pars.behav_obs_count(data, affiliative_interactions)
behav_obs_summary.loc[:, 'Mean duration per observation'] = behav_obs_summary.loc[:,'Total duration'] / behav_obs_summary.loc[:,'Total count']
# edge_list pour les non-orientés : toujours non-symetrique. Pose question de si bien reciproque ?
pars.edge_list(data, social_behaviors)
pars.adj_table(data, directed_interaction,
               social_behaviors, indiv, undir_adj_table=True)
# mettre en dict, dissocier les calculs de taux, l'empty diagonal.
behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                     directed_interaction, social_behaviors, indiv, undir_adj_table=True)
affiliative_behavior_rate_dict = pars.table_dict(data, affiliative_interactions,
                                                 directed_interaction, affiliative_interactions, indiv, undir_adj_table=True)
# dsi
behavior_rate_list = list(affiliative_behavior_rate_dict.values())
behav_obs_time = pars.behav_obs_time(data, affiliative_interactions)
behav_obs_count = pars.behav_obs_count(data, affiliative_interactions)
tot_obs = pars.tot_obs_time(data)
dsi = constr.dsi_table2(
    behavior_rate_list, indiv, affiliative_interactions, behav_obs_time, tot_obs)
behavior_rate_dict['dsi'] = dsi

"""
#partie visualisation clustermap.
seaborn.clustermap(behavior_rate_dict['Grooming'], method='complete',
                   metric='euclidean', dendrogram_ratio={0, 0.2}, cbar_pos=(0.9, 0.85, 0.05, 0.18),  cmap="Reds")
plt.show()
"""
"""save
with pd.ExcelWriter('../Data/layers_' + dataset_name + '.xlsx') as writer:
    for df_name, df in behavior_rate_dict.items():
        df.to_excel(writer, sheet_name=df_name)
behav_obs_summary.to_excel('behav_obs_summary_' + dataset_name + '.xlsx')
"""
